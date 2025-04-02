import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection to your server.py
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Your server script
    env=None,  # Optional environment variables
)

async def test_login():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools (optional, for verification)
            tools = await session.list_tools()
            print(f"Available tools: {tools}")
            
            # Navigate to the website
            result = await session.call_tool("playwright_navigate", arguments={
                "url": "http://eaapp.somee.com/"
            })
            print("Navigation result:", result.text if hasattr(result, 'text') else result)
            
            # Click on the login link
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "Login"
            })
            print("Click login link result:", result.text if hasattr(result, 'text') else result)
            
            # Fill in username
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "#UserName",
                "value": "admin"
            })
            print("Fill username result:", result.text if hasattr(result, 'text') else result)
            
            # Fill in password
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "#Password",
                "value": "password"
            })
            print("Fill password result:", result.text if hasattr(result, 'text') else result)
            
            # Click login button
            result = await session.call_tool("playwright_click", arguments={
                "selector": "input[value='Log in']"
            })
            print("Click login button result:", result.text if hasattr(result, 'text') else result)
            
            # Get text content to verify login success
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("Page content after login:", result.text if hasattr(result, 'text') else result)

if __name__ == "__main__":
    asyncio.run(test_login())