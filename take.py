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
            await asyncio.sleep(5)  # Increased delay to ensure page loads
            
            # Get page content to inspect elements
            result = await session.call_tool("playwright_evaluate", arguments={
                "expression": """
                    () => {
                        // Get all visible elements that might be title placeholders
                        const elements = Array.from(document.querySelectorAll('div, span, [contenteditable="true"]'));
                        return elements.map(el => ({
                            tag: el.tagName,
                            id: el.id,
                            className: el.className,
                            text: el.innerText,
                            isEditable: el.isContentEditable,
                            rect: el.getBoundingClientRect()
                        })).filter(info => 
                            info.text.includes('title') || 
                            info.text.includes('Title') || 
                            info.isEditable
                        );
                    }
                """
            })
            print("Page elements:", result.text(result))
            
            # Try different selectors for the title
            selectors_to_try = [
                "[contenteditable='true']",
                ".title-placeholder",
                ".slide-title",
                "[aria-label*='title']",
                "[placeholder*='title']",
                ".pptx-slide-title"
            ]
            
            title_found = False
            for selector in selectors_to_try:
                try:
                    # Check if selector exists
                    check_result = await session.call_tool("playwright_evaluate", arguments={
                        "expression": f"() => document.querySelector('{selector}') !== null"
                    })
                    
                    if check_result.text(check_result) == "true":
                        print(f"Found selector: {selector}")
                        result = await session.call_tool("playwright_fill", arguments={
                            "selector": selector,
                            "value": "PPT Agent Demo"
                        })
                        print(f"Fill title result with {selector}:", result.text(result))
                        title_found = True
                        break
                except Exception as e:
                    print(f"Error with selector {selector}:", e)
            
            if not title_found:
                # Try clicking in the center of the slide where title usually is
                try:
                    result = await session.call_tool("playwright_evaluate", arguments={
                        "expression": """
                            () => {
                                // Try to click in the upper part of the slide where title usually is
                                const centerX = window.innerWidth / 2;
                                const centerY = window.innerHeight / 3;
                                const element = document.elementFromPoint(centerX, centerY);
                                if (element) {
                                    element.click();
                                    return {clicked: true, element: element.tagName, id: element.id, class: element.className};
                                }
                                return {clicked: false};
                            }
                        """
                    })
                    print("Click result:", result.text(result))
                    
                    # Try typing after clicking
                    result = await session.call_tool("playwright_keyboard_type", arguments={
                        "text": "PPT Agent Demo"
                    })
                    print("Keyboard type result:", result.text(result))
                except Exception as e:
                    print("Error with manual click:", e)
            
            # Take a final screenshot
            result = await session.call_tool("playwright_screenshot", arguments={
                "name": "powerpoint_final"
            })
            print("Final screenshot taken")

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
