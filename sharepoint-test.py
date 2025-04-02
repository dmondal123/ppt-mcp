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
            
            # Try to click on "Click to add title" text first
            try:
                result = await session.call_tool("playwright_click_text", arguments={
                    "text": "Click to add title"
                })
                print("Click title placeholder result:", result.text if hasattr(result, 'text') else result)
                
                # Wait a moment for the editor to focus
                await asyncio.sleep(1)
                
                # Try to type directly
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": """
                    // Simulate typing "ppt agent"
                    document.execCommand('insertText', false, 'ppt agent');
                    return "Text inserted via execCommand";
                    """
                })
                print("Direct typing result:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error clicking title placeholder:", e)
            
            # Try using JavaScript to set the title specifically targeting NormalTextRun
            try:
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": """
                    // Try to find and modify the NormalTextRun span
                    const normalTextRuns = document.querySelectorAll('.NormalTextRun');
                    if (normalTextRuns.length > 0) {
                        // Find the parent container that might be the title
                        let titleContainer = normalTextRuns[0];
                        let parent = normalTextRuns[0].parentElement;
                        
                        // Go up a few levels to find a suitable container
                        for (let i = 0; i < 5; i++) {
                            if (parent && (
                                parent.getAttribute('aria-label')?.includes('title') || 
                                parent.className?.includes('title') ||
                                parent.role === 'heading'
                            )) {
                                titleContainer = parent;
                                break;
                            }
                            if (parent) parent = parent.parentElement;
                        }
                        
                        // Set the text content
                        titleContainer.textContent = 'ppt agent';
                        return "Title set via NormalTextRun";
                    }
                    
                    // If no NormalTextRun found, try to find the title placeholder
                    const titlePlaceholders = Array.from(document.querySelectorAll('*')).filter(el => 
                        el.textContent?.includes('Click to add title') || 
                        el.getAttribute('aria-label')?.includes('title')
                    );
                    
                    if (titlePlaceholders.length > 0) {
                        titlePlaceholders[0].textContent = 'ppt agent';
                        return "Title set via placeholder";
                    }
                    
                    return "No NormalTextRun or title placeholder found";
                    """
                })
                print("JavaScript title result:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error with JavaScript:", e)
            
            # Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
