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
            await asyncio.sleep(1)
            #Try to click on "Click to add title" text first
            try:
                # First try to click on the element
                click_result = await session.call_tool("playwright_click", arguments={
                    "selector": "span.NormalTextRun"
                })
                print("Click on span.NormalTextRun result:", click_result.text(click_result))
                
                # Try to fill it after clicking
                fill_result = await session.call_tool("playwright_fill", arguments={
                    "selector": "span.NormalTextRun",
                    "value": "ppt agent"
                })
                print("Fill title result:", fill_result.text(fill_result))
                
                # If direct fill doesn't work, try typing after clicking
                type_result = await session.call_tool("playwright_type", arguments={
                    "text": "ppt agent via keyboard"
                })
                print("Keyboard type result:", type_result.text(type_result))
                
                # Try clicking on parent elements
                parent_selectors = [
                    "div.title-placeholder",
                    "div.slide-title",
                    "[contenteditable='true']",
                    "[role='textbox']"
                ]
                
                for selector in parent_selectors:
                    try:
                        parent_click = await session.call_tool("playwright_click", arguments={
                            "selector": selector
                        })
                        print(f"Click on {selector} result:", parent_click.text(parent_click))
                        
                        parent_type = await session.call_tool("playwright_type", arguments={
                            "text": f"ppt agent via {selector}"
                        })
                        print(f"Type in {selector} result:", parent_type.text(parent_type))
                        
                        # Take a screenshot after each attempt
                        screenshot = await session.call_tool("playwright_screenshot", arguments={
                            "name": f"after_{selector.replace('[', '').replace(']', '').replace('=', '_').replace('\'', '')}"
                        })
                        print(f"Screenshot taken after {selector}")
                    except Exception as e:
                        print(f"Error with {selector}:", e)
                
                # Try clicking at different positions on the slide
                positions = [
                    {"x": 400, "y": 150},  # Top center
                    {"x": 400, "y": 200},  # Upper center
                    {"x": 400, "y": 250}   # Middle center
                ]
                
                for i, pos in enumerate(positions):
                    try:
                        position_click = await session.call_tool("playwright_mouse_click", arguments={
                            "x": pos["x"],
                            "y": pos["y"]
                        })
                        print(f"Click at position ({pos['x']}, {pos['y']}) result:", position_click.text(position_click))
                        
                        position_type = await session.call_tool("playwright_type", arguments={
                            "text": f"ppt agent at position {i+1}"
                        })
                        print(f"Type at position {i+1} result:", position_type.text(position_type))
                        
                        # Take a screenshot after each position attempt
                        screenshot = await session.call_tool("playwright_screenshot", arguments={
                            "name": f"after_position_{i+1}"
                        })
                        print(f"Screenshot taken after position {i+1}")
                    except Exception as e:
                        print(f"Error with position {i+1}:", e)
                
            except Exception as e:
                print("Error interacting with title placeholder:", e)
                
            # Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={ 
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
