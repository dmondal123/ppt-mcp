import asyncio
import json
import aiohttp
import uuid
import sys

async def send_command(session, base_url, session_id, method, params=None):
    """Send a command to the MCP server and return the response."""
    if params is None:
        params = {}
    
    command = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": params
    }
    
    url = f"{base_url}/jsonrpc?sessionId={session_id}"
    print(f"Sending command to {url}: {method}")
    try:
        headers = {"Content-Type": "application/json"}
        async with session.post(url, json=command, headers=headers, timeout=30) as response:
            print(f"Response status: {response.status}")
            if response.status == 202:
                print("Command accepted (202 status)")
                return {"status": "accepted"}
            
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            if 'json' in content_type:
                return await response.json()
            else:
                text = await response.text()
                print(f"Response text: {text[:200]}...")
                try:
                    return json.loads(text)
                except:
                    return {"status": "success", "text": text[:100]}
    except Exception as e:
        print(f"Error with endpoint: {e}")
        return {"error": str(e)}

async def sharepoint_create_presentation():
    base_url = "http://localhost:9222"
    
    print(f"Connecting to {base_url}...")
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            print("Fetching initial page to get session ID...")
            try:
                async with session.get(f"{base_url}", timeout=10) as response:
                    print(f"Response status: {response.status}")
                    
                    chunk = await response.content.read(1024)
                    text = chunk.decode('utf-8')
                    print(f"Response chunk: {text}")
                    
                    import re
                    match = re.search(r'sessionId=([0-9a-f-]+)', text)
                    
                    if match:
                        session_id = match.group(1)
                        print(f"Using session ID: {session_id}")
                        
                        # Initialize a new browser context
                        print("Initializing browser context...")
                        result = await send_command(session, base_url, session_id, "initialize", {
                            "capabilities": {}
                        })
                        print(f"Initialize result: {result}")
                        
                        # Navigate to SharePoint
                        print("Navigating to SharePoint...")
                        result = await send_command(session, base_url, session_id, "Playwright_navigate", {
                            "url": "https://www.office.com/launch/powerpoint",
                            "browserType": "chromium",
                            "width": 1280,
                            "height": 720,
                            "headless": False
                        })
                        print(f"Navigation result: {result}")
                        
                        # Wait for page to load
                        await asyncio.sleep(5)
                        
                        # Check if login is required
                        print("Checking if login is required...")
                        visible_text = await send_command(session, base_url, session_id, "playwright_get_visible_text", {})
                        if "Sign in" in visible_text.get("content", ""):
                            print("Login required. Please sign in manually within 30 seconds...")
                            # Give user time to log in manually
                            await asyncio.sleep(30)
                        
                        # Click on "New blank presentation" or "+ New blank presentation"
                        print("Clicking on New blank presentation...")
                        result = await send_command(session, base_url, session_id, "Playwright_click", {
                            "selector": "button:has-text('New blank presentation'), div:has-text('New blank presentation')"
                        })
                        print(f"Click result: {result}")
                        
                        # Wait for PowerPoint to load
                        print("Waiting for PowerPoint to load...")
                        await asyncio.sleep(10)
                        
                        # Click on "New Slide" button
                        print("Adding a new slide...")
                        result = await send_command(session, base_url, session_id, "Playwright_click", {
                            "selector": "button[aria-label='New Slide'], button:has-text('New Slide')"
                        })
                        print(f"New slide result: {result}")
                        
                        # Wait for slide to be added
                        await asyncio.sleep(3)
                        
                        # Click on the title placeholder to edit it
                        print("Clicking on title placeholder...")
                        result = await send_command(session, base_url, session_id, "Playwright_click", {
                            "selector": "div[aria-label='Title'], div.title"
                        })
                        print(f"Click on title result: {result}")
                        
                        # Clear existing text and type new title
                        print("Typing new title...")
                        result = await send_command(session, base_url, session_id, "Playwright_fill", {
                            "selector": "div[aria-label='Title'], div.title",
                            "value": "ppt agent"
                        })
                        print(f"Title change result: {result}")
                        
                        # Take a screenshot to verify
                        print("Taking screenshot...")
                        result = await send_command(session, base_url, session_id, "Playwright_screenshot", {
                            "name": "powerpoint_result",
                            "fullPage": True,
                            "savePng": True,
                            "downloadsDir": "."
                        })
                        print(f"Screenshot result: {result}")
                        
                        print("PowerPoint presentation created successfully!")
                    else:
                        print("Could not find session ID in the response")
            except Exception as e:
                print(f"Error during SharePoint automation: {e}")
    except Exception as e:
        print(f"Session creation error: {e}")

if __name__ == "__main__":
    # Install required packages if not already installed
    import subprocess
    try:
        import aiohttp
    except ImportError:
        print("Installing aiohttp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
        print("aiohttp installed successfully")
    
    asyncio.run(sharepoint_create_presentation())