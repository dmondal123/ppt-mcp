import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection to your server.py
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Your server script
    env=None,  # Optional environment variables
)

async def test_iframe_interaction():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools (optional, for verification)
            tools = await session.list_tools()
            print(f"Available tools: {tools}")
            
            # Navigate to the HTML page served by http-server
            result = await session.call_tool("playwright_navigate", arguments={
                "url": "http://localhost:8080/"  # Update this to match your http-server URL
            })
            print("Navigation result:", result)
            
            # Take a screenshot of the initial page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "initial_page"
            })
            print("Initial screenshot taken")
            
            # Switch to the iframe
            result = await session.call_tool("playwright_frame", arguments={
                "name": "editor_frame"
            })
            print(f"Switched to iframe: {result}")
            
            # Wait for the iframe content to fully load
            result = await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 1000  # Wait 1 second
            })
            print(f"Waited for iframe to load: {result}")
            
            # Take a screenshot inside the iframe
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "inside_iframe"
            })
            print("Screenshot taken inside iframe")
            
            # Click on the text input field
            result = await session.call_tool("playwright_click", arguments={
                "selector": "#nameInput"
            })
            print(f"Click on text input: {result}")
            
            # Clear the existing text and fill with "Diya"
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "#nameInput",
                "value": "Diya"
            })
            print(f"Fill text input with 'Diya': {result}")
            
            # Wait a moment for the change to register
            result = await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 1000  # Wait 1 second
            })
            print(f"Waited after input: {result}")
            
            # Take a final screenshot to verify the change
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "after_name_change"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_iframe_interaction())
