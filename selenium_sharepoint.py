import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def login_and_create_presentation():
    # Set up Chrome options
    chrome_options = Options()
    # Uncomment the line below if you want to run headless
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to SharePoint
        print("Navigating to SharePoint...")
        driver.get("https://visainc-my.sharepoint.com/")
        
        # Take a screenshot of the initial page
        driver.save_screenshot("office_home.png")
        print("Screenshot taken of initial page")
        
        # Click on Sign in
        print("Clicking Sign in...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Sign in')]"))
        ).click()
        
        # Take a screenshot of the login page
        driver.save_screenshot("login_page.png")
        print("Screenshot taken of login page")
        
        # Enter email/username
        print("Entering email...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        ).send_keys("diymonda@visa.com")  # Replace with actual email
        
        # Click Next
        print("Clicking Next...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        ).click()
        
        # Enter password
        print("Entering password...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        ).send_keys("your_password")  # Replace with actual password
        
        # Click Sign in
        print("Clicking Sign in...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        ).click()
        
        # Wait for the page to load
        time.sleep(5)
        
        # Click on "New" button
        print("Clicking New button...")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New')]"))
        ).click()
        
        # Click on PowerPoint presentation
        print("Clicking PowerPoint presentation...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'PowerPoint presentation')]"))
        ).click()
        
        # Wait for the PowerPoint editor to load
        print("Waiting for PowerPoint editor to load...")
        time.sleep(10)
        
        # Take a screenshot before editing
        driver.save_screenshot("powerpoint_before_edit.png")
        print("Screenshot taken before editing")
        
        # Switch to the PowerPoint iframe
        print("Switching to PowerPoint iframe...")
        iframe = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "WacFrame_PowerPoint_0"))
        )
        driver.switch_to.frame(iframe)
        
        # Find and click on the title placeholder
        print("Clicking on title placeholder...")
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Click to add title')]"))
        ).click()
        
        # Wait a moment for the editor to activate
        time.sleep(1)
        
        # Find the active editable element and set its text
        print("Setting title text...")
        # Using JavaScript to set the text of the active element
        driver.execute_script("""
        const activeElement = document.activeElement;
        if (activeElement && activeElement.isContentEditable) {
            activeElement.textContent = "PPT Agent";
        }
        """)
        
        # Take a screenshot after editing
        driver.save_screenshot("powerpoint_after_edit.png")
        print("Screenshot taken after editing")
        
        # Wait to see the result
        time.sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("error.png")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    login_and_create_presentation() 