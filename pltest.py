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
        
        # Click on "New" button
        try:
            await page.get_by_text("New").click()
            print("Clicked New button")
        except Exception as e:
            print(f"Error clicking New button: {e}")
        
        # Click on PowerPoint presentation
        try:
            await page.get_by_text("PowerPoint presentation").click()
            print("Clicked PowerPoint presentation")
        except Exception as e:
            print(f"Error clicking PowerPoint presentation: {e}")
        
        # Wait for the PowerPoint editor to load
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(5)  # Additional delay to ensure editor loads
        
        # Take a screenshot of the PowerPoint editor
        await page.screenshot(path="powerpoint_editor.png")
        print("PowerPoint editor screenshot taken")
        
        # Try different selectors for the title
        selectors_to_try = [
            "[contenteditable='true']",
            ".title-placeholder",
            ".slide-title",
            "[aria-label*='title']",
            "[placeholder*='title']",
            ".pptx-slide-title",
            "[data-automation-id*='title']",
            "[role='textbox']"
        ]
        
        title_found = False
        for selector in selectors_to_try:
            try:
                # Check if selector exists
                element = await page.query_selector(selector)
                if element:
                    print(f"Found selector: {selector}")
                    
                    # Get the text content for debugging
                    text_content = await element.text_content()
                    print(f"Element text: {text_content}")
                    
                    # Try to fill the element
                    await element.fill("PPT Agent Demo")
                    print(f"Filled title with {selector}")
                    title_found = True
                    break
            except Exception as e:
                print(f"Error with selector {selector}: {e}")
        
        if not title_found:
            # Try clicking in the center of the slide where title usually is
            try:
                # Get viewport size
                viewport_size = page.viewport_size
                center_x = viewport_size["width"] // 2
                center_y = viewport_size["height"] // 3
                
                # Click where the title should be
                await page.mouse.click(center_x, center_y)
                print(f"Clicked at position ({center_x}, {center_y})")
                
                # Type the title
                await page.keyboard.type("PPT Agent Demo")
                print("Typed title text")
            except Exception as e:
                print(f"Error with manual click and type: {e}")
        
        # Take a final screenshot
        await page.screenshot(path="powerpoint_final.png")
        print("Final screenshot taken")
        
        # Print only editable elements on the page for debugging
        try:
            print("Trying alternative methods to find editable elements...")
            
            # Method 1: Look for elements with specific attributes that might indicate editability
            potential_editable_selectors = [
                "[contenteditable]",
                "[role='textbox']",
                "[aria-multiline='true']",
                "input:not([type='hidden'])",
                "textarea",
                "[data-slate-editor]",
                "[data-automation-id*='title']",
                "[data-automation-id*='edit']",
                "[class*='title']",
                "[class*='edit']"
            ]
            
            for selector in potential_editable_selectors:
                elements = await page.query_selector_all(selector)
                if elements:
                    print(f"Found {len(elements)} elements with selector: {selector}")
                    for i, element in enumerate(elements[:5]):  # Limit to first 5 elements per selector
                        try:
                            tag_name = await element.evaluate("el => el.tagName")
                            text_content = await element.text_content()
                            
                            # Get attributes
                            id_attr = await element.get_attribute("id") or ""
                            class_attr = await element.get_attribute("class") or ""
                            aria_label = await element.get_attribute("aria-label") or ""
                            
                            print(f"Potential Editable Element {i+1} with selector {selector}: {tag_name}")
                            print(f"  Text: {text_content[:50]}{'...' if len(text_content) > 50 else ''}")
                            print(f"  ID: {id_attr}")
                            print(f"  Class: {class_attr}")
                            print(f"  Aria-label: {aria_label}")
                            print("---")
                        except Exception as e:
                            print(f"Error getting element info: {e}")
            
            # Method 2: Try to identify elements by their position
            print("Checking elements at typical title positions...")
            viewport_size = page.viewport_size
            center_x = viewport_size["width"] // 2
            
            # Check elements at different vertical positions where titles might be
            for y_pos in [viewport_size["height"] // 4, viewport_size["height"] // 3, viewport_size["height"] // 2]:
                try:
                    # Get element at this position
                    element = await page.evaluate(f"""
                        () => {{
                            const element = document.elementFromPoint({center_x}, {y_pos});
                            if (element) {{
                                return {{
                                    tag: element.tagName,
                                    id: element.id || "",
                                    class: element.className || "",
                                    ariaLabel: element.getAttribute('aria-label') || "",
                                    text: element.innerText || "",
                                    position: "{center_x}, {y_pos}"
                                }};
                            }}
                            return null;
                        }}
                    """)
                    
                    if element:
                        print(f"Element at position ({center_x}, {y_pos}):")
                        print(f"  Tag: {element.get('tag')}")
                        print(f"  Text: {element.get('text')[:50]}{'...' if len(element.get('text', '')) > 50 else ''}")
                        print(f"  ID: {element.get('id')}")
                        print(f"  Class: {element.get('class')}")
                        print(f"  Aria-label: {element.get('ariaLabel')}")
                        print("---")
                except Exception as e:
                    print(f"Error checking position ({center_x}, {y_pos}): {e}")
            
            # Method 3: Try to interact with the title area directly
            print("Attempting direct interaction with title area...")
            try:
                # Click where the title should be
                title_y = viewport_size["height"] // 3
                await page.mouse.click(center_x, title_y)
                
                # Try to type and see if it works
                await page.keyboard.type("Test Title")
                
                # Take a screenshot to see if typing worked
                await page.screenshot(path="title_typing_test.png")
                print("Typed 'Test Title' at position ({center_x}, {title_y}) - check title_typing_test.png")
            except Exception as e:
                print(f"Error with direct interaction: {e}")
                
        except Exception as e:
            print(f"Error in alternative methods: {e}")
        
        # Close browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_sharepoint_login())
