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
            print("Navigation result:", get_result_text(result))
            
            # Take a screenshot of the initial page
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "office_home"
            })
            print("Screenshot taken")
            
            # Click on Sign in
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "Sign in"
            })
            print("Click sign in result:", get_result_text(result))
            
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
            print("Fill email result:", get_result_text(result))
            
            # Click Next
            result = await session.call_tool("playwright_click", arguments={
                "selector": "input[type='submit']"
            })
            print("Click next result:", get_result_text(result))
            
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
            print("Fill password result:", get_result_text(result))
            
            # Take a screenshot of the Office home page after login
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "after_login"
            })
            print("Screenshot taken")
            
            # Navigate to SharePoint
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "SharePoint"
            })
            print("Navigate to SharePoint result:", get_result_text(result))
            
            # Take a screenshot of SharePoint
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "sharepoint_home"
            })
            print("Screenshot taken")
            
            # Click on "New" button
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "New"
            })
            print("Click New button result:", get_result_text(result))
            
            # Take a screenshot of the New menu
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "new_menu"
            })
            print("Screenshot taken")
            
            # Get the current pages before clicking
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": "window.initialUrl = window.location.href; 'Stored initial URL'"
            })
            print("Stored initial URL:", result)
            
            # Click on PowerPoint presentation
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "PowerPoint presentation"
            })
            print("Click PowerPoint presentation result:", get_result_text(result))
            
            # Wait for the PowerPoint editor to load
            # Adding a small delay to ensure the editor loads properly
            await asyncio.sleep(5)
            
            # Check if we're still on the same page
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": "window.location.href === window.initialUrl ? 'Same page' : 'New page'"
            })
            result_text = get_result_text(result)
            print("Page check:", result)
            print("Page result:", result_text)
            
            # Switch to the new tab if we're still on the same page
            if "Same page" in result_text:
                # List all pages/tabs
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "window.open('about:blank', '_blank'); 'Opened new tab'"
                })
                print("Open new tab result:", get_result_text(result))
                
                # Switch to the new tab
                result = await session.call_tool("playwright_switch_tab", arguments={
                    "index": 1  # Switch to the second tab (index 1)
                })
                print("Switch tab result:", get_result_text(result))
                
                # Navigate directly to the PowerPoint editor URL
                result = await session.call_tool("playwright_navigate", arguments={
                    "url": "https://visainc-my.sharepoint.com/personal/diymonda_visa_com/_layouts/15/Doc.aspx?sourcedoc={}&action=edit"
                })
                print("Direct navigation result:", get_result_text(result))
            
            # Take a screenshot of the PowerPoint editor
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_editor"
            })
            print("Screenshot taken")
            
            # Get text content to see what's available
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("PowerPoint editor content:", result)
            
            # Try using playwright_fill with different selectors
            try:
                # Try with div.ShapeViewContent
                result = await session.call_tool("playwright_fill", arguments={
                    "selector": "div.ShapeViewContent",
                    "value": "ppt agent"
                })
                print("Fill ShapeViewContent result:", get_result_text(result))
            except Exception as e:
                print("Error filling ShapeViewContent:", e)
                
                try:
                    # Try with div.Paragraph.WhiteSpaceCollapse
                    result = await session.call_tool("playwright_fill", arguments={
                        "selector": "div.Paragraph.WhiteSpaceCollapse",
                        "value": "ppt agent"
                    })
                    print("Fill Paragraph.WhiteSpaceCollapse result:", get_result_text(result))
                except Exception as e:
                    print("Error filling Paragraph.WhiteSpaceCollapse:", e)
                    
                    try:
                        # Try with XPath
                        result = await session.call_tool("playwright_fill", arguments={
                            "selector": "//div[contains(@class, 'ShapeViewContent')]",
                            "value": "ppt agent"
                        })
                        print("Fill XPath result:", get_result_text(result))
                    except Exception as e:
                        print("Error filling with XPath:", e)
                        
                        try:
                            # Try with a more general selector
                            result = await session.call_tool("playwright_fill", arguments={
                                "selector": "[contenteditable='true']",
                                "value": "ppt agent"
                            })
                            print("Fill contenteditable result:", get_result_text(result))
                        except Exception as e:
                            print("Error filling contenteditable:", e)
            
            # Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

def get_result_text(result):
    """Helper function to safely extract text from result objects"""
    try:
        if hasattr(result, 'content') and result.content:
            for content in result.content:
                if hasattr(content, 'text'):
                    return content.text
        return str(result)
    except Exception as e:
        return f"Error extracting text: {e}"

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
