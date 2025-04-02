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
            
            # Get the current pages before clicking
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": "window.initialUrl = window.location.href; 'Stored initial URL'"
            })
            print("Stored initial URL:", result.text if hasattr(result, 'text') else result)
            
            # Click on PowerPoint presentation
            result = await session.call_tool("playwright_click_text", arguments={
                "text": "PowerPoint presentation"
            })
            print("Click PowerPoint presentation result:", result.text if hasattr(result, 'text') else result)
            
            # Wait for the PowerPoint editor to load
            # Adding a small delay to ensure the editor loads properly
            await asyncio.sleep(5)
            
            # Check if we're still on the same page
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": "window.location.href === window.initialUrl ? 'Same page' : 'New page'"
            })
            print("Page check:", result.text if hasattr(result, 'text') else result)
            
            # Switch to the new tab if we're still on the same page
            if "Same page" in result.text:
                # List all pages/tabs
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "window.open('about:blank', '_blank'); 'Opened new tab'"
                })
                print("Open new tab result:", result.text if hasattr(result, 'text') else result)
                
                # Switch to the new tab
                result = await session.call_tool("playwright_switch_tab", arguments={
                    "index": 1  # Switch to the second tab (index 1)
                })
                print("Switch tab result:", result.text if hasattr(result, 'text') else result)
                
                # Navigate directly to the PowerPoint editor URL
                result = await session.call_tool("playwright_navigate", arguments={
                    "url": "https://visainc-my.sharepoint.com/personal/diymonda_visa_com/_layouts/15/Doc.aspx?sourcedoc={}&action=edit"
                })
                print("Direct navigation result:", result.text if hasattr(result, 'text') else result)
            
            # Take a screenshot of the PowerPoint editor
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_editor"
            })
            print("Screenshot taken")
            
            # Get text content to see what's available
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("PowerPoint editor content:", result.text if hasattr(result, 'text') else result)
            
            # Try to find ShapeViewContent
            try:
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "document.querySelector('div.ShapeViewContent') ? 'Found ShapeViewContent' : 'Not found'"
                })
                print("ShapeViewContent check:", result.text if hasattr(result, 'text') else result)
                
                if "Found" in result.text:
                    # Try to set text content
                    result = await session.call_tool("playwright_evaluate", arguments={
                        "script": "document.querySelector('div.ShapeViewContent').textContent = 'ppt agent'; 'Text set'"
                    })
                    print("Set ShapeViewContent text:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error with ShapeViewContent:", e)
            
            # Try to find Paragraph.WhiteSpaceCollapse
            try:
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "document.querySelector('div.Paragraph.WhiteSpaceCollapse') ? 'Found Paragraph.WhiteSpaceCollapse' : 'Not found'"
                })
                print("Paragraph.WhiteSpaceCollapse check:", result.text if hasattr(result, 'text') else result)
                
                if "Found" in result.text:
                    # Try to set text content
                    result = await session.call_tool("playwright_evaluate", arguments={
                        "script": "document.querySelector('div.Paragraph.WhiteSpaceCollapse').textContent = 'ppt agent'; 'Text set'"
                    })
                    print("Set Paragraph.WhiteSpaceCollapse text:", result.text if hasattr(result, 'text') else result)
            except Exception as e:
                print("Error with Paragraph.WhiteSpaceCollapse:", e)
            
            # Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
