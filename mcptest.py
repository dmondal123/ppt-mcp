import asyncio
import aiohttp
import sys
import json
import time

async def simple_http_get(session, url, timeout=10):
    """Make a simple HTTP GET request with a timeout."""
    print(f"GET request to: {url}")
    try:
        async with session.get(url, timeout=timeout) as response:
            print(f"Response status: {response.status}")
            
            # Try to read just a small amount of data
            try:
                # Read only first 1000 bytes to avoid streaming issues
                data = await response.content.read(1000)
                print(f"Received {len(data)} bytes")
                return response.status, data
            except Exception as e:
                print(f"Error reading response data: {e}")
                return response.status, None
    except asyncio.TimeoutError:
        print(f"Timeout requesting {url}")
        return None, None
    except Exception as e:
        print(f"Error requesting {url}: {e}")
        return None, None

async def test_connection():
    """Test if we can connect to the Chrome DevTools endpoint."""
    base_url = "http://localhost:9222"
    
    print(f"Testing connection to {base_url}...")
    
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Try different endpoints to check what kind of server we're connecting to
        endpoints = [
            "/",
            "/json",
            "/json/version",
            "/json/list",
            "/json/new?about:blank",
            "/devtools/inspector.html",
            "/devtools/page/"
        ]
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            status, data = await simple_http_get(session, url)
            
            print(f"Endpoint {endpoint}: status={status}")
            
            if status == 200 and data:
                try:
                    # Try to decode as JSON if possible
                    if data.startswith(b"{") or data.startswith(b"["):
                        json_data = json.loads(data)
                        print(f"JSON data: {json.dumps(json_data, indent=2)[:500]}...")
                    else:
                        print(f"Data (first 100 bytes): {data[:100]}")
                except:
                    print(f"Non-JSON data (first 100 bytes): {data[:100]}")
                    
        print("\nTrying direct navigational URL...")
        # Try direct navigation to the test website
        test_url = "http://eaapp.somee.com/"
        print(f"Directly testing access to {test_url}")
        status, data = await simple_http_get(session, test_url)
        
        if status == 200:
            print(f"Successfully accessed {test_url}")
            if data:
                print(f"First 100 bytes: {data[:100]}")
        else:
            print(f"Failed to access {test_url}")
        
        print("\nConnection tests completed")

if __name__ == "__main__":
    # Install required packages if not already installed
    import subprocess
    try:
        import aiohttp
    except ImportError:
        print("Installing aiohttp...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
        print("aiohttp installed successfully")
    
    asyncio.run(test_connection())
