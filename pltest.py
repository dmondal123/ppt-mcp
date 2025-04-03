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
        
        # Specifically check the span.NormalTextRun element
        print("Checking if span.NormalTextRun is editable...")
        try:
            # Find the span.NormalTextRun element
            span_element = await page.query_selector("span.NormalTextRun")
            
            if span_element:
                # Get text content
                text_content = await span_element.text_content()
                print(f"Found span.NormalTextRun with text: {text_content}")
                
                # Check if the element itself is editable
                is_element_editable = await span_element.is_editable()
                print(f"Is span.NormalTextRun directly editable: {is_element_editable}")
                
                # Try to click on it
                await span_element.click()
                print("Clicked on span.NormalTextRun")
                
                # Try to type after clicking
                await page.keyboard.type("PPT Agent Demo")
                print("Typed text after clicking span.NormalTextRun")
                
                # Take a screenshot
                await page.screenshot(path="after_normalTextRun_click.png")
                
                # Try to find parent elements that might be editable
                parent_element = await page.evaluate("""
                    selector => {
                        const element = document.querySelector(selector);
                        if (!element) return null;
                        
                        // Find closest potentially editable parent
                        let parent = element.parentElement;
                        let path = [];
                        
                        while (parent) {
                            path.push({
                                tag: parent.tagName,
                                id: parent.id || "",
                                class: parent.className || "",
                                isEditable: parent.isContentEditable
                            });
                            
                            if (parent.isContentEditable) break;
                            parent = parent.parentElement;
                        }
                        
                        return path;
                    }
                """, "span.NormalTextRun")
                
                if parent_element:
                    print("Parent element hierarchy:")
                    for i, parent in enumerate(parent_element):
                        print(f"  Level {i+1}: {parent.get('tag')} (ID: {parent.get('id')}, Class: {parent.get('class')}, Editable: {parent.get('isEditable')})")
                        
                        # If we found an editable parent, try to use its selector
                        if parent.get('isEditable'):
                            parent_id = parent.get('id')
                            parent_class = parent.get('class')
                            
                            if parent_id:
                                parent_selector = f"#{parent_id}"
                            elif parent_class:
                                parent_selector = f".{parent_class.replace(' ', '.')}"
                            else:
                                continue
                            
                            print(f"Trying to interact with editable parent using selector: {parent_selector}")
                            
                            try:
                                parent_element = await page.query_selector(parent_selector)
                                if parent_element:
                                    await parent_element.click()
                                    await page.keyboard.type("PPT Agent Demo via Parent")
                                    await page.screenshot(path=f"after_parent_{i+1}_click.png")
                            except Exception as e:
                                print(f"Error interacting with parent {i+1}: {e}")
            else:
                print("Could not find span.NormalTextRun element")
                
                # Try to find any elements with NormalTextRun in their class
                elements_with_normal_text = await page.query_selector_all("[class*='NormalTextRun']")
                print(f"Found {len(elements_with_normal_text)} elements with NormalTextRun in their class")
                
                for i, element in enumerate(elements_with_normal_text):
                    text = await element.text_content()
                    print(f"Element {i+1} text: {text}")
                    
                    # Check if this element is editable
                    is_editable = await element.is_editable()
                    print(f"Element {i+1} is editable: {is_editable}")
                    
                    # Try to click and type
                    await element.click()
                    await page.keyboard.type(f"PPT Agent Demo {i+1}")
                    await page.screenshot(path=f"after_normalTextRun_variant_{i+1}_click.png")
        except Exception as e:
            print(f"Error checking span.NormalTextRun: {e}")
        
        # Close browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
