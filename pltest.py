import asyncio
from playwright.async_api import async_playwright

async def test_sharepoint_login():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Navigate to SharePoint login page
        await page.goto("https://visainc-my.sharepoint.com/")
        print("Navigated to SharePoint")
        
        # Take a screenshot of the initial page
        await page.screenshot(path="office_home.png")
        print("Screenshot taken")
        
        # Click on Sign in
        try:
            await page.get_by_text("Sign in").click()
            print("Clicked sign in")
        except Exception as e:
            print(f"Error clicking sign in: {e}")
        
        # Take a screenshot of the login page
        await page.screenshot(path="login_page.png")
        print("Screenshot taken")
        
        # Enter email/username
        try:
            await page.fill("input[type='email']", "diymonda@visa.com")  # Replace with actual email
            print("Filled email")
        except Exception as e:
            print(f"Error filling email: {e}")
        
        # Click Next
        try:
            await page.click("input[type='submit']")
            print("Clicked next")
        except Exception as e:
            print(f"Error clicking next: {e}")
        
        # Enter password
        try:
            await page.fill("input[type='password']", "your_password")  # Replace with actual password
            print("Filled password")
            await page.click("input[type='submit']")
            print("Clicked sign in")
        except Exception as e:
            print(f"Error filling password: {e}")
        
        # Wait for the page to load
        await page.wait_for_load_state("networkidle")
        print("Page loaded after login")
        
        # Take a screenshot after login
        await page.screenshot(path="after_login.png")
        
        # Navigate directly to the PowerPoint editor URL
        try:
            await page.goto("https://visainc-my.sharepoint.com/personal/diymonda_visa_com/_layouts/15/Doc.aspx?sourcedoc={}&action=edit")
            print("Navigated directly to PowerPoint editor")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(5)  # Additional delay to ensure editor loads
        except Exception as e:
            print(f"Error navigating to PowerPoint editor: {e}")
        
        # Take a screenshot of the PowerPoint editor
        await page.screenshot(path="powerpoint_editor.png")
        print("PowerPoint editor screenshot taken")
        
        # Print page title and URL for debugging
        title = await page.title()
        url = page.url
        print(f"Page title: {title}")
        print(f"Current URL: {url}")
        
        # Look specifically for the "Click to add title" element
        print("Looking for 'Click to add title' element...")
        try:
            # Try to find the element by text content
            title_locator = page.get_by_text("Click to add title")
            count = await title_locator.count()
            print(f"Found {count} elements with text 'Click to add title'")
            
            if count > 0:
                title_element = await title_locator.first
                print("Found 'Click to add title' element by text")
                
                # Try to click on it
                await title_element.click()
                print("Clicked on 'Click to add title' element")
                
                # Try to type after clicking
                await page.keyboard.type("PPT Agent Demo")
                print("Typed title text after clicking")
                
                # Take a screenshot
                await page.screenshot(path="after_title_click.png")
            else:
                print("No 'Click to add title' elements found, trying alternative methods")
                
                # Try to find elements with text containing "title"
                title_related_locator = page.get_by_text("title", exact=False)
                count = await title_related_locator.count()
                print(f"Found {count} elements with text containing 'title'")
                
                if count > 0:
                    for i in range(count):
                        element = await title_related_locator.nth(i)
                        text = await element.text_content()
                        print(f"Element {i+1} text: {text}")
                        
                        # Try to click on it
                        await element.click()
                        print(f"Clicked on element {i+1}")
                        
                        # Try to type after clicking
                        await page.keyboard.type("PPT Agent Demo")
                        print("Typed title text after clicking")
                        
                        # Take a screenshot
                        await page.screenshot(path=f"after_title_related_{i+1}_click.png")
                        break
                else:
                    # Try clicking in the center of the slide where title usually is
                    viewport_size = page.viewport_size
                    center_x = viewport_size["width"] // 2
                    center_y = viewport_size["height"] // 3
                    
                    # Click where the title should be
                    await page.mouse.click(center_x, center_y)
                    print(f"Clicked at position ({center_x}, {center_y})")
                    
                    # Try to type after clicking
                    await page.keyboard.type("PPT Agent Demo")
                    print("Typed title text after clicking")
                    
                    # Take a screenshot
                    await page.screenshot(path="after_position_click.png")
        except Exception as e:
            print(f"Error finding and interacting with title element: {e}")
        
        # Try to find any editable elements
        try:
            # Look for common editable elements
            editable_selectors = [
                "[contenteditable='true']",
                "[role='textbox']",
                "div[class*='title']",
                "div[class*='slide-title']",
                "div[class*='placeholder']"
            ]
            
            for selector in editable_selectors:
                elements = await page.query_selector_all(selector)
                print(f"Found {len(elements)} elements with selector: {selector}")
                
                if elements:
                    for i, element in enumerate(elements[:3]):  # Limit to first 3 elements
                        text = await element.text_content()
                        print(f"Element {i+1} with selector {selector} text: {text}")
                        
                        # Try to click and type
                        await element.click()
                        await page.keyboard.type("PPT Agent Demo")
                        print(f"Clicked and typed in element {i+1} with selector {selector}")
                        
                        # Take a screenshot
                        await page.screenshot(path=f"after_{selector.replace('[', '').replace(']', '').replace('*', '').replace('=', '_').replace('\"', '')}_click_{i+1}.png")
                        break
        except Exception as e:
            print(f"Error finding editable elements: {e}")
        
        # Close browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
