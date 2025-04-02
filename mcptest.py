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
    
    # Try different endpoints
    endpoints = [
        f"{base_url}/jsonrpc?sessionId={session_id}"
    ]
    
    for url in endpoints:
        print(f"Trying to send command to {url}: {method}")
        try:
            headers = {"Content-Type": "application/json"}
            async with session.post(url, json=command, headers=headers, timeout=10) as response:
                print(f"Response status: {response.status}")
                if response.status == 202:
                    # 202 Accepted means the command was accepted but no content is returned
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
                        # Try to parse as JSON anyway
                        return json.loads(text)
                    except:
                        return {"status": "success", "text": text[:100]}
        except Exception as e:
            print(f"Error with endpoint {url}: {e}")
    
    return {"error": "All endpoints failed"}

async def test_login():
    base_url = "http://localhost:9222"
    
    print(f"Connecting to {base_url}...")
    try:
        # Create a session with a longer timeout
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # First, get the session ID
            print("Fetching initial page to get session ID...")
            try:
                async with session.get(f"{base_url}", timeout=5) as response:
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
                        
                        # Navigate to the website
                        print("Navigating to website...")
                        result = await send_command(session, base_url, session_id, "Playwright_navigate", {
                            "url": "http://eaapp.somee.com/"
                        })
                        print(f"Navigation result: {result}")
                        
                        # Wait a bit for the page to load
                        await asyncio.sleep(2)
                        
                        # Click on the login link
                        print("Clicking login link...")
                        result = await send_command(session, base_url, session_id, "Playwright_click", {
                            "selector": "a:has-text('Login')"
                        })
                        print(f"Click result: {result}")
                        
                        # Wait a bit for the page to load
                        await asyncio.sleep(1)
                        
                        # Fill in username
                        print("Filling username...")
                        result = await send_command(session, base_url, session_id, "Playwright_fill", {
                            "selector": "input[name='UserName']",
                            "value": "admin"
                        })
                        print(f"Username fill result: {result}")
                        
                        # Fill in password
                        print("Filling password...")
                        result = await send_command(session, base_url, session_id, "Playwright_fill", {
                            "selector": "input[name='Password']",
                            "value": "password"
                        })
                        print(f"Password fill result: {result}")
                        
                        # Click login button
                        print("Clicking login button...")
                        result = await send_command(session, base_url, session_id, "Playwright_click", {
                            "selector": "input[type='submit']"
                        })
                        print(f"Login button click result: {result}")
                        
                        print("Login completed successfully")
                    else:
                        print("Could not find session ID in the response")
            except Exception as e:
                print(f"Error during login process: {e}")
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
    
    asyncio.run(test_login())
