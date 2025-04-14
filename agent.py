import asyncio
import os
import re
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import openai

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Create server parameters for stdio connection to your server.py
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Your server script
    env=None,  # Optional environment variables
)

class WebAutomationAgent:
    def __init__(self):
        self.session = None
        self.conversation_history = []
        self.available_tools = []
        
    async def initialize(self):
        # Connect to the MCP server and initialize the session
        read, write = await stdio_client(server_params).__aenter__()
        self.session = await ClientSession(read, write).__aenter__()
        await self.session.initialize()
        
        # Get available tools
        self.available_tools = await self.session.list_tools()
        print(f"Available tools: {[tool.name for tool in self.available_tools]}")
        
        # Add system message to conversation history
        self.conversation_history.append({
            "role": "system",
            "content": self._create_system_prompt()
        })
    
    def _create_system_prompt(self):
        # Create a system prompt that describes the available tools
        tool_descriptions = []
        for tool in self.available_tools:
            desc = f"- {tool.name}: {tool.description}"
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                required = tool.inputSchema.get('required', [])
                properties = tool.inputSchema.get('properties', {})
                params = []
                for param_name, param_info in properties.items():
                    req = " (required)" if param_name in required else ""
                    desc_text = param_info.get('description', '')
                    params.append(f"  - {param_name}{req}: {desc_text}")
                if params:
                    desc += "\n" + "\n".join(params)
            tool_descriptions.append(desc)
        
        return f"""You are a web automation assistant that helps users navigate websites and perform tasks.
You have access to the following Playwright tools:

{chr(10).join(tool_descriptions)}

When the user gives you an instruction, break it down into steps and execute each step using the appropriate tool.
For each step, explain what you're doing and show the result.
If you encounter an error, try alternative approaches or ask the user for clarification.
"""
    
    async def process_user_instruction(self, user_instruction):
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_instruction
        })
        
        # Get AI response
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=self.conversation_history,
            temperature=0.2,
        )
        
        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Parse and execute the actions from the AI response
        actions = self._parse_actions(assistant_message)
        results = []
        
        for action in actions:
            tool_name = action.get('tool')
            arguments = action.get('arguments', {})
            
            if not tool_name:
                results.append(f"Info: {action.get('info', 'No action specified')}")
                continue
                
            print(f"Executing: {tool_name} with arguments {arguments}")
            try:
                result = await self.session.call_tool(tool_name, arguments)
                results.append(f"Result of {tool_name}: {result}")
                
                # Add the result to conversation history
                self.conversation_history.append({
                    "role": "system",
                    "content": f"Action: {tool_name}({arguments})\nResult: {result}"
                })
                
                # If this is a screenshot, let the user know
                if tool_name == "playwright_screenshot":
                    print(f"Screenshot saved as {arguments.get('name', 'screenshot')}.png")
                
                # If this is a manual action prompt, wait for user input
                if "MANUAL ACTION REQUIRED" in str(result):
                    input("Press Enter when the manual action is completed...")
                    
            except Exception as e:
                error_message = f"Error executing {tool_name}: {str(e)}"
                results.append(error_message)
                self.conversation_history.append({
                    "role": "system",
                    "content": error_message
                })
        
        return results
    
    def _parse_actions(self, message):
        # Parse actions from the AI message
        # Look for patterns like:
        # 1. Use playwright_navigate to go to the URL
        # ```
        # playwright_navigate({"url": "https://example.com"})
        # ```
        
        actions = []
        
        # First, try to find code blocks with tool calls
        code_block_pattern = r"```(?:python)?\s*(?:await\s+)?(?:session\.)?call_tool\([\"']([^\"']+)[\"'],\s*(?:arguments=)?(\{[^}]+\})\)"
        code_blocks = re.findall(code_block_pattern, message, re.DOTALL)
        
        for tool_name, args_str in code_blocks:
            try:
                # Clean up the args string and convert to dict
                args_str = args_str.replace("'", '"')
                import json
                arguments = json.loads(args_str)
                actions.append({
                    "tool": tool_name,
                    "arguments": arguments
                })
            except Exception as e:
                print(f"Error parsing arguments: {e}")
                actions.append({
                    "info": f"Could not parse arguments for {tool_name}: {args_str}"
                })
        
        # If no code blocks found, look for simpler patterns
        if not actions:
            # Look for tool names and try to extract arguments
            for tool in self.available_tools:
                if tool.name in message:
                    # Try to find arguments in the same paragraph
                    paragraph = re.search(f"[^.]*{tool.name}[^.]*", message)
                    if paragraph:
                        # Extract URL if present
                        url_match = re.search(r"https?://[^\s\"']+", paragraph.group(0))
                        if url_match and "url" in str(tool.inputSchema):
                            actions.append({
                                "tool": tool.name,
                                "arguments": {"url": url_match.group(0)}
                            })
                        # Extract selector if present
                        selector_match = re.search(r"selector [\"']([^\"']+)[\"']", paragraph.group(0))
                        if selector_match and "selector" in str(tool.inputSchema):
                            actions.append({
                                "tool": tool.name,
                                "arguments": {"selector": selector_match.group(1)}
                            })
                        # Extract text if present
                        text_match = re.search(r"text [\"']([^\"']+)[\"']", paragraph.group(0))
                        if text_match and "text" in str(tool.inputSchema):
                            actions.append({
                                "tool": tool.name,
                                "arguments": {"text": text_match.group(1)}
                            })
        
        # If still no actions found, add an info message
        if not actions:
            actions.append({
                "info": "No specific actions found in the message. Please provide more details."
            })
        
        return actions
    
    async def close(self):
        # Close the session and connection
        if self.session:
            await self.session.__aexit__(None, None, None)

async def main():
    agent = WebAutomationAgent()
    await agent.initialize()
    
    print("\nWeb Automation Agent initialized!")
    print("You can now give instructions like:")
    print("- Navigate to outlook.office.com/calendar")
    print("- Click on the meeting with title 'Demo Microsoft Meeting'")
    print("- Download the resume.txt file from the wiki page")
    print("\nType 'exit' to quit.")
    
    try:
        while True:
            user_input = input("\nEnter your instruction: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
                
            results = await agent.process_user_instruction(user_input)
            for result in results:
                print(result)
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())
