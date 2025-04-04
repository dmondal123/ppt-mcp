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
            await asyncio.sleep(5)  # Increased delay to ensure editor fully loads
            
            # Try to switch to the new tab by evaluating all pages and switching to the last one
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": """
                (async () => {
                    // This will run in the browser context
                    const pages = await window.browsingContext.pages();
                    if (pages.length > 1) {
                        await pages[pages.length - 1].bringToFront();
                        return "Switched to new tab: " + window.location.href;
                    }
                    return "No new tab found: " + window.location.href;
                })()
                """
            })
            print(f"Tab switch result: {result}")
            
            # Print the current URL after attempting to switch tabs
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": "window.location.href"
            })
            print(f"Current URL after tab switch attempt: {result}")
            
            # Take a screenshot to verify we're on the correct page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "after_tab_switch"
            })
            print("Screenshot taken after tab switch attempt")
            
            # Get text content to help debug
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print(f"Page content before inserting slide: {result}")
            
            #Click on "Insert" tab in the ribbon
            try:
                result = await session.call_tool("playwright_click_text", arguments={
                    "text": "Insert"
                })
                print("Click on Insert tab result:", result.text if hasattr(result, 'text') else result)
                
                #Click on "New Slide" button
                result = await session.call_tool("playwright_click_text", arguments={
                    "text": "New Slide"
                })
                print("Click on New Slide result:", result.text if hasattr(result, 'text') else result)
                
                #Take a screenshot after adding new slide
                result = await session.call_tool("playwright_screenshot", arguments={
                    "name": "new_slide_added"
                })
                print("New slide screenshot taken")
            except Exception as e:
                print("Error adding new slide:", e)
            
            #Try to click on "Click to add title" text first
            try:
                result = await session.call_tool("playwright_fill", arguments={
                "selector": "span.NormalTextRun",
                "value": "ppt agent"
                })
                print("Click to add title:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error clicking title placeholder:", e)
                
            #Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={ "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
