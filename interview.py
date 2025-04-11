import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import re

# Create server parameters for stdio connection to your server.py
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Your server script
    env=None,  # Optional environment variables
)

async def run_interview():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Step 1: Navigate to Outlook Calendar
            print("Navigating to Outlook Calendar...")
            result = await session.call_tool("playwright_navigate", arguments={
                "url": "outlook.office.com/calendar/view/workweek"
            })
            print("Navigation result:", result.text(result))
            
            # Step 2: Wait for login page to load
            print("Waiting for login page to load...")
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 3000
            })
            
            # Step 3: Take a screenshot to see the login page
            await session.call_tool("playwright_screenshot", arguments={
                "name": "login_page"
            })
            print("Screenshot taken")
            
            # Step 4: Get text content to see what's on the page
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("Page content:", result.text(result))
            
            # Step 5: Prompt user to complete the login manually
            print("\n*** MANUAL ACTION REQUIRED ***")
            print("Please complete the login process in the browser window.")
            print("The script will continue after you press Enter...")
            input()
            
            # Step 6: Wait for calendar to load after login
            print("Waiting for calendar to load...")
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 5000
            })
            await session.call_tool("playwright_screenshot", arguments={
                "name": "calendar_page"
            })
            print("Screenshot taken")
            
            # Step 7: Find and click on the meeting with title "Demo Microsoft Meeting"
            print("Looking for 'Demo Microsoft Meeting'...")
            try:
                result = await session.call_tool("playwright_click_text", arguments={
                    "text": "Demo Microsoft Meeting"
                })
                print("Meeting found and clicked!")
            except Exception as e:
                print(f"Error clicking meeting: {e}")
                print("Taking screenshot to debug...")
                await session.call_tool("playwright_screenshot", arguments={
                    "name": "calendar_error"
                })
            
            # Step 8: Wait for meeting details to load
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 3000
            })
            await session.call_tool("playwright_screenshot", arguments={
                "name": "meeting_details"
            })
            print("Screenshot taken")
            
            # Step 9: Extract text to find the wiki URL
            result = await session.call_tool("playwright_get_text_content", arguments={})
            print("Meeting details:", result.text(result))
            
            # Step 10: Use JavaScript to find and extract the URL from the span element
            print("Extracting wiki URL from meeting details...")
            result = await session.call_tool("playwright_evaluate", arguments={
                "script": """
                    // Try to find the element using the specific selector
                    const element = document.querySelector("div:nth-of-type(8) div.VSXvP span");
                    if (element && element.textContent) {
                        // Extract URL from the span's text content
                        const text = element.textContent.trim();
                        // Check if it looks like a URL
                        if (text.startsWith('http') || text.includes('wiki')) {
                            return text;
                        }
                    }
                """
            })
            
            # Extract just the URL from the result
            result_str = str(result)
            wiki_url = None
            
            # Look for a URL pattern in the result string
            url_match = re.search(r'https?://[^\s\'"]+', result_str)
            if url_match:
                wiki_url = url_match.group(0)
            else:
                # If regex fails, try a simpler approach
                parts = result_str.split('result = ')
                if len(parts) > 1:
                    wiki_url = parts[1].split(',')[0].strip().rstrip("'").rstrip('"')
                else:
                    wiki_url = result_str
            
            if not wiki_url or wiki_url == "null":
                print("No wiki URL found in the meeting details")
                return
            
            print(f"Found wiki URL: {wiki_url}")
            
            # Step 11: Navigate to the wiki URL
            print(f"Navigating to wiki page: {wiki_url}")
            result = await session.call_tool("playwright_navigate", arguments={
                "url": wiki_url
            })
            
            # Step 12: Wait for wiki page to load and handle potential SSO login
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 3000
            })
            await session.call_tool("playwright_screenshot", arguments={
                "name": "wiki_page"
            })
            print("Screenshot taken")
            
            # Step 13: Check if we need to login again
            result = await session.call_tool("playwright_get_text_content", arguments={})
            result_text = result.text(result)
            if "login" in result_text.lower() or "sign in" in result_text.lower():
                print("\n*** MANUAL ACTION REQUIRED ***")
                print("Please complete the SSO login for the wiki page.")
                print("The script will continue after you press Enter...")
                input()
                await session.call_tool("playwright_wait_for_timeout", arguments={
                    "timeout": 5000
                })
            
            # Step 14: Look for resume.txt file and download it
            print("Looking for resume.txt file...")
            await session.call_tool("playwright_screenshot", arguments={
                "name": "wiki_loaded"
            })
            print("Screenshot taken")
            
            # Try to find and click on the resume.txt link
            try:
                result = await session.call_tool("playwright_click_text", arguments={
                    "text": "resume.txt"
                })
                print("Found and clicked resume.txt link!")
            except Exception as e:
                print(f"Error finding resume.txt: {e}")
                
                # Alternative approach: try to find by evaluating JavaScript
                result = await session.call_tool("playwright_evaluate", arguments={
                    "script": """
                        // Find links that contain resume.txt
                        const links = Array.from(document.querySelectorAll('a')).filter(a => 
                            a.textContent.includes('resume.txt') || 
                            a.href.includes('resume.txt')
                        );
                        if (links.length > 0) {
                            links[0].click();
                            return "Clicked resume.txt link via JavaScript";
                        }
                        return "No resume.txt link found";
                    """
                })
                print(result.text(result))
            
            # Step 15: Wait for download to complete
            print("Waiting for download to complete...")
            await session.call_tool("playwright_wait_for_timeout", arguments={
                "timeout": 5000
            })
            
            print("Interview process completed!")
            print("Check your downloads folder for resume.txt")

if __name__ == "__main__":
    asyncio.run(run_interview())
