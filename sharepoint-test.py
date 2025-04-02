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
                "value": "diymonda@visa.com"  # Replace with actual email
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
            
            # Get text content to see what's available
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("PowerPoint editor content:", result.text if hasattr(result, 'text') else result)
            
            # Try to click on any visible element that might be the title
            try:
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": """
                    function findAndClickTitle() {
                        // Try different selectors that might be the title
                        const selectors = [
                            'div.ShapeViewContent',
                            'div.Paragraph.WhiteSpaceCollapse',
                            '[aria-label*="title"]',
                            '[placeholder*="title"]',
                            '[contenteditable="true"]',
                            '.title-placeholder',
                            '.pptx-slide-title'
                        ];
                        
                        for (const selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            for (const element of elements) {
                                if (element.offsetWidth > 0 && element.offsetHeight > 0) {
                                    // Element is visible, try to click it
                                    element.click();
                                    // Try to set text content
                                    element.textContent = 'ppt agent';
                                    return `Clicked and set text on ${selector}`;
                                }
                            }
                        }
                        
                        // If no specific title element found, try to find any element with "Click to add title" text
                        const allElements = document.querySelectorAll('*');
                        for (const element of allElements) {
                            if (element.textContent && element.textContent.includes('Click to add title')) {
                                element.click();
                                element.textContent = 'ppt agent';
                                return 'Clicked and set text on element with "Click to add title" text';
                            }
                        }
                        
                        return 'No suitable title element found';
                    }
                    
                    return findAndClickTitle();
                    """
                })
                print("Find, click and set title result:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error with JavaScript:", e)
            
            # Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
