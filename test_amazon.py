from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_amazon_search(browser_name="chrome"):
    # Launch browser
    if browser_name.lower() == "chrome":
        driver = webdriver.Chrome()
    elif browser_name.lower() == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError("Only 'chrome' and 'firefox' are supported.")

    try:
        driver.maximize_window()

        # 1. Navigation
        driver.get("https://www.amazon.com.tr")

        wait = WebDriverWait(driver, 15)

        # 2. Accept cookies if the button is present
        try:
            accept_cookies = wait.until(EC.element_to_be_clickable((By.ID, "sp-cc-accept")))
            accept_cookies.click()
        except:
            pass  # Cookie popup not shown

        # 3. Checking title
        assert "Amazon" in driver.title, f"Unexpected title: {driver.title}"
        print("✅ Page title verified.")

        # 4. Typing text in the search box
        # Wait for the Amazon logo to ensure page is fully loaded
        wait.until(EC.presence_of_element_located((By.ID, "nav-logo-sprites")))

        # Then safely locate the search bar
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
        search_input.clear()
        search_input.send_keys("kulaklık")  # "headphones" in Turkish

        # 5. Clicking the search button
        search_input.send_keys(Keys.ENTER)

        # 6. Wait for search results to appear
        results_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
        )
        print("✅ Search results loaded.")

        # 7. Selecting an item from results and taking action (e.g., clicking)
        first_item = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']"))
        )
        first_item.click()
        print("✅ First search result clicked.")

        # Optional: wait for product title to verify navigation to product page
        product_title = wait.until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )
        print(f"✅ Product page loaded: {product_title.text.strip()}")

        input("🔍 Press Enter to close the browser...")

    finally:
        driver.quit()


# Run the test
if __name__ == "__main__":
    # Replace with "firefox" to test in Firefox
    test_amazon_search("Chrome")