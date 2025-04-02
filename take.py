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
                "url": "https://visainc-my.sharepoint.com/"
            })
            print("Navigation result:", result.text(result))
            
            # Take a screenshot of the initial page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "office_home"
            })
            print("Screenshot taken")
            
            # Click on Sign in
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "Sign in"
            })
            print("Click sign in result:", result.text(result))
            
            # Take a screenshot of the login page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "login_page"
            })
            print("Screenshot taken")
            
            # Enter email/username
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "input[type='email']",
                "value": "diymonda@visa.com"  # Replace with actual email
            })

            print("Fill email result:", result.text if hasattr(result, 'text') else result)
            # Click Next
            result = await session.call_tool("playwright_click", arguments={
                "selector": "input[type='submit']"
            })
            print("Click next result:", result.text(result))
            #Click on "New" button
            result = await session.call_tool("playwright_fill", arguments={
                "selector": "input[type='password']",
                "value": "your_password"  # Replace with actual password
            })
            print("Click New button result:", result.text if hasattr(result, 'text') else result)
            #Click on PowerPoint presentation
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "PowerPoint presentation"
            })
            print("Click PowerPoint presentation result:", result.text if hasattr(result, 'text') else result)
            #Wait for the PowerPoint editor to load
            #Adding a small delay to ensure the editor loads properly
            await asyncio.sleep(5)  # Increased delay to ensure editor fully loads
            
            # Take a screenshot to see the current state
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_editor"
            })
            print("PowerPoint editor screenshot taken")
            
            # Try to interact with the title element using JavaScript evaluation
            try:
                # First, get text content to see what's available
                result = await session.call_tool("playwright_get_text_content", arguments={})
                print("Available text elements:", result.text if hasattr(result, 'text') else result)
                
                # Try to click on the title area first
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": """
                    // Try to find and click the title element
                    const titleElements = Array.from(document.querySelectorAll('span.NormalTextRun, [aria-label*="title"], [placeholder*="title"], [aria-label*="Title"], [placeholder*="Title"]'));
                    const titleElement = titleElements.find(el => el.offsetWidth > 0 && el.offsetHeight > 0);
                    if (titleElement) {
                        titleElement.click();
                        return "Title element clicked";
                    } else {
                        return "No visible title element found";
                    }
                    """
                })
                print("Click title result:", result.text if hasattr(result, 'text') else result)
                
                # Now try to type into the focused element
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": """
                    // Try to set text content for the active/focused element
                    if (document.activeElement) {
                        document.activeElement.textContent = "PPT Agent";
                        return "Text set on active element";
                    } else {
                        return "No active element found";
                    }
                    """
                })
                print("Set title text result:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error interacting with title:", e)
                
            #Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={ 
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
