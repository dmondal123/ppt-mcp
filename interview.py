import asyncio
import time
from mcp.client import Client

async def run_interview():
    # Connect to the MCP server
    client = Client()
    await client.connect()
    
    # Step 1: Navigate to Outlook Calendar
    print("Navigating to Outlook Calendar...")
    result = await client.call_tool(
        "playwright_navigate", 
        {"url": "outlook.office.com/calendar/view/workweek"}
    )
    print(result)
    
    # Step 2: Wait for login page to load
    print("Waiting for login page to load...")
    await client.call_tool("playwright_wait_for_timeout", {"timeout": 3000})
    
    # Step 3: Take a screenshot to see the login page
    await client.call_tool("playwright_screenshot", {"name": "login_page"})
    
    # Step 4: Get text content to see what's on the page
    result = await client.call_tool("playwright_get_text_content", {})
    print("Page content:", result)
    
    # Step 5: Prompt user to complete the login manually
    print("\n*** MANUAL ACTION REQUIRED ***")
    print("Please complete the login process in the browser window.")
    print("The script will continue after you press Enter...")
    input()
    
    # Step 6: Wait for calendar to load after login
    print("Waiting for calendar to load...")
    await client.call_tool("playwright_wait_for_timeout", {"timeout": 5000})
    await client.call_tool("playwright_screenshot", {"name": "calendar_page"})
    
    # Step 7: Find and click on the meeting with title "Demo Microsoft Meeting"
    print("Looking for 'Demo Microsoft Meeting'...")
    try:
        await client.call_tool("playwright_click_text", {"text": "Demo Microsoft Meeting"})
        print("Meeting found and clicked!")
    except Exception as e:
        print(f"Error clicking meeting: {e}")
        print("Taking screenshot to debug...")
        await client.call_tool("playwright_screenshot", {"name": "calendar_error"})
    
    # Step 8: Wait for meeting details to load
    await client.call_tool("playwright_wait_for_timeout", {"timeout": 3000})
    await client.call_tool("playwright_screenshot", {"name": "meeting_details"})
    
    # Step 9: Extract text to find the wiki URL
    result = await client.call_tool("playwright_get_text_content", {})
    print("Meeting details:", result)
    
    # Step 10: Use JavaScript to find and extract the URL
    print("Extracting wiki URL from meeting details...")
    result = await client.call_tool(
        "playwright_evaluate", 
        {"script": """
            // Find all links in the meeting body
            const links = Array.from(document.querySelectorAll('a[href*="wiki"]'));
            return links.length > 0 ? links[0].href : null;
        """}
    )
    
    if not result or "null" in str(result):
        print("No wiki URL found in the meeting details")
        return
    
    wiki_url = result[0].text.strip() if hasattr(result[0], 'text') else str(result).strip()
    print(f"Found wiki URL: {wiki_url}")
    
    # Step 11: Navigate to the wiki URL
    print(f"Navigating to wiki page: {wiki_url}")
    await client.call_tool("playwright_navigate", {"url": wiki_url})
    
    # Step 12: Wait for wiki page to load and handle potential SSO login
    await client.call_tool("playwright_wait_for_timeout", {"timeout": 3000})
    await client.call_tool("playwright_screenshot", {"name": "wiki_page"})
    
    # Step 13: Check if we need to login again
    result = await client.call_tool("playwright_get_text_content", {})
    if "login" in str(result).lower() or "sign in" in str(result).lower():
        print("\n*** MANUAL ACTION REQUIRED ***")
        print("Please complete the SSO login for the wiki page.")
        print("The script will continue after you press Enter...")
        input()
        await client.call_tool("playwright_wait_for_timeout", {"timeout": 5000})
    
    # Step 14: Look for resume.txt file and download it
    print("Looking for resume.txt file...")
    await client.call_tool("playwright_screenshot", {"name": "wiki_loaded"})
    
    # Try to find and click on the resume.txt link
    try:
        await client.call_tool("playwright_click_text", {"text": "resume.txt"})
        print("Found and clicked resume.txt link!")
    except Exception as e:
        print(f"Error finding resume.txt: {e}")
        
        # Alternative approach: try to find by evaluating JavaScript
        result = await client.call_tool(
            "playwright_evaluate", 
            {"script": """
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
            """}
        )
        print(result)
    
    # Step 15: Wait for download to complete
    print("Waiting for download to complete...")
    await client.call_tool("playwright_wait_for_timeout", {"timeout": 5000})
    
    print("Interview process completed!")
    print("Check your downloads folder for resume.txt")

if __name__ == "__main__":
    asyncio.run(run_interview())
