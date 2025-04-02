import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Create server parameters for stdio connection to your server.py
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Your server script
    env=None,  # Optional environment variables
)

async def test_sharepoint_login():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools (optional, for verification)
            tools = await session.list_tools()
            print(f"Available tools: {tools}")
            
            # Navigate to SharePoint login page
            result = await session.call_tool("playwright_navigate", arguments={
                "url": "https://www.office.com/"
            })
            print("Navigation result:", result.text if hasattr(result, 'text') else result)
            
            # Take a screenshot of the initial page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "office_home"
            })
            print("Screenshot taken")
            
            # Click on Sign in
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "Sign in"
            })
            print("Click sign in result:", result.text if hasattr(result, 'text') else result)
            
            # Take a screenshot of the login page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "login_page"
            })
            print("Screenshot taken")
            
            # Enter email/username
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "input[type='email']",
                "value": "your_email@example.com"  # Replace with actual email
            })
            print("Fill email result:", result.text if hasattr(result, 'text') else result)
            
            # Click Next
            result = await session.call_tool("playwright_click", arguments={
                "selector": "input[type='submit']"
            })
            print("Click next result:", result.text if hasattr(result, 'text') else result)
            
            # Take a screenshot of the password page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "password_page"
            })
            print("Screenshot taken")
            
            # Enter password
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "input[type='password']",
                "value": "your_password"  # Replace with actual password
            })
            print("Fill password result:", result.text if hasattr(result, 'text') else result)
            
            # Click Sign in
            result = await session.call_tool("playwright_click", arguments={
                "selector": "input[type='submit']"
            })
            print("Click sign in result:", result.text if hasattr(result, 'text') else result)
            
            # Handle "Stay signed in?" prompt if it appears
            try:
                result = await session.call_tool("playwright_click", arguments={
                    "selector": "input[id='idSIButton9']"  # "Yes" button
                })
                print("Clicked 'Stay signed in':", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("No 'Stay signed in' prompt or error:", e)
            
            # Take a screenshot of the Office home page after login
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "after_login"
            })
            print("Screenshot taken")
            
            # Navigate to SharePoint
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "SharePoint"
            })
            print("Navigate to SharePoint result:", result.text if hasattr(result, 'text') else result)
            
            # Take a screenshot of SharePoint
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "sharepoint_home"
            })
            print("Screenshot taken")
            
            # Click on "New" button
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "New"
            })
            print("Click New button result:", result.text if hasattr(result, 'text') else result)
            
            # Take a screenshot of the New menu
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "new_menu"
            })
            print("Screenshot taken")
            
            # Click on PowerPoint presentation
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "PowerPoint presentation"
            })
            print("Click PowerPoint presentation result:", result.text if hasattr(result, 'text') else result)
            
            # Wait for the PowerPoint editor to load
            # Adding a small delay to ensure the editor loads properly
            await asyncio.sleep(5)
            
            # Take a screenshot of the PowerPoint editor
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_editor"
            })
            print("Screenshot taken")
            
            # Enter title "ppt agent"
            # First, we need to click on the title placeholder
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "Click to add title"
            })
            print("Click title placeholder result:", result.text if hasattr(result, 'text') else result)
            
            # Now type the title
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "div[aria-label='Title text']",
                "value": "ppt agent"
            })
            print("Enter title result:", result.text if hasattr(result, 'text') else result)
            
            # Take a final screenshot of the PowerPoint with title
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_with_title"
            })
            print("Screenshot taken")
            
            # Get text content to verify successful creation
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("PowerPoint editor content:", result.text if hasattr(result, 'text') else result)

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
