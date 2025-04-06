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
            
            # List all available pages/tabs
            result = await session.call_tool("playwright_list_pages", arguments={})
            print(f"Available pages: {result}")
            
            # Try to switch to each available page and check if it's the PowerPoint editor
            # First get the number of pages
            pages_info = str(result)
            page_count = pages_info.count("Page ")
            print(f"Detected {page_count} pages")
            
            powerpoint_page_found = False
            for i in range(page_count):
                # Switch to this page
                result = await session.call_tool("playwright_switch_to_page", arguments={
                    "index": i
                })
                print(f"Switched to page {i}: {result}")
                
                # Check if this is the PowerPoint page
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "document.title"
                })
                page_title = str(result)
                print(f"Page {i} title: {page_title}")
                
                # Take a screenshot of this page
                result = await session.call_tool("playwright_screenshot", arguments={
                    "name": f"page_{i}"
                })
                print(f"Screenshot taken of page {i}")
                
                if "PowerPoint" in page_title or "presentation" in page_title.lower():
                    print(f"Found PowerPoint editor on page {i}")
                    powerpoint_page_found = True
                    break
            
            if not powerpoint_page_found:
                print("PowerPoint editor page not found in any tab")
                # As a last resort, try the last page
                if page_count > 1:
                    result = await session.call_tool("playwright_switch_to_page", arguments={
                        "index": page_count - 1
                    })
                    print(f"Switched to last page as fallback: {result}")
            
            # Now try to click on "Insert" tab in the ribbon
            try:
                # First, let's identify all iframes on the page
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "document.querySelectorAll('iframe').length"
                })
                print(f"Number of iframes on page: {result}")
                
                # Get iframe details (just IDs and names)
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": "Array.from(document.querySelectorAll('iframe')).map(iframe => ({id: iframe.id, name: iframe.name}))"
                })
                print(f"Iframe details: {result}")
                
                # Take a screenshot for reference
                result = await session.call_tool("playwright_screenshot", arguments={
                    "name": "before_iframe_interaction"
                })
                print("Screenshot taken before iframe interaction")
                
                # Try to get HTML content of the page
                result = await session.call_tool("playwright_get_html_content", arguments={
                    "selector": "body"
                })
                print(f"Page body HTML (first 500 chars): {str(result)[:500]}...")
                
                # Try to get HTML content of each iframe
                for i in range(int(str(result).split(":")[-1].strip()) if ":" in str(result) and str(result).split(":")[-1].strip().isdigit() else 0):
                    try:
                        # Get HTML content of this iframe
                        iframe_selector = f"iframe:nth-of-type({i+1})"
                        result = await session.call_tool("playwright_get_html_content", arguments={
                            "selector": iframe_selector
                        })
                        print(f"Iframe {i} HTML: {result}")
                    except Exception as e:
                        print(f"Error getting iframe {i} content: {e}")
                
                # First switch to the PowerPoint iframe
                try:
                    result = await session.call_tool("playwright_frame", arguments={
                        "name": "WacFrame_PowerPoint_0"
                    })
                    print(f"Switched to PowerPoint iframe: {result}")
                    
                    # Wait for the iframe content to fully load
                    result = await session.call_tool("playwright_wait_for_timeout", arguments={
                        "timeout": 3000  # Wait 3 seconds
                    })
                    print(f"Waited for iframe to load: {result}")
                    
                    # Take a screenshot to see what we're working with
                    result = await session.call_tool("playwright_screenshot", arguments={
                        "name": "powerpoint_before_edit"
                    })
                    print("Screenshot taken before editing")
                    
                    # First, let's find all elements that might be editable
                    result = await session.call_tool("playwright_evaluate", arguments={
                        "script": """
                        // Find all elements that might be editable
                        const editableElements = Array.from(document.querySelectorAll('[contenteditable="true"]'));
                        const elementsInfo = editableElements.map(el => ({
                            tagName: el.tagName,
                            id: el.id,
                            className: el.className,
                            text: el.textContent.substring(0, 100)
                        }));
                        elementsInfo;
                        """
                    })
                    print(f"Editable elements: {result}")
                    
                    # Now try to click on the title placeholder
                    result = await session.call_tool("playwright_click", arguments={
                        "selector": "[contenteditable='true']:has-text('Click to add title')"
                    })
                    print(f"Click on title placeholder: {result}")
                    
                    # Wait a moment for the click to register
                    result = await session.call_tool("playwright_wait_for_timeout", arguments={
                        "timeout": 1000  # Wait 1 second
                    })
                    print(f"Waited after click: {result}")
                    
                    # Now try to type directly after clicking
                    result = await session.call_tool("playwright_evaluate", arguments={
                        "script": """
                        // Get the active element and set its text content
                        const activeElement = document.activeElement;
                        let status = "No editable element is active";
                        if (activeElement && activeElement.isContentEditable) {
                            activeElement.textContent = "PPT Agent";
                            status = "Text set successfully";
                        }
                        status;
                        """
                    })
                    print(f"Set title text: {result}")
                    
                    # Take a screenshot to see if it worked
                    result = await session.call_tool("playwright_screenshot", arguments={
                        "name": "powerpoint_after_edit"
                    })
                    print("Screenshot taken after editing")
                    
                except Exception as e:
                    print(f"Error with iframe operations: {e}")
            
            except Exception as e:
                print(f"Error during PowerPoint interaction: {e}")
            
            #Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
