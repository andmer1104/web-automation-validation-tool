import os
import tempfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


USERNAME = "standard_user"
PASSWORD = "secret_sauce"
FIRST_NAME = "Andy"
LAST_NAME = "Mera"
POSTAL_CODE = "56560"


def start_browser():
    print("[1] Starting browser...")

    chrome_options = Options()

    # Use a fresh temporary Chrome profile each run
    temp_profile = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_profile}")

    # Try to reduce Chrome interruptions
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver


def wait_for_element(driver, by, value, timeout=10):
    print(f"[DEBUG] Waiting for element: {value}")
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def login(driver):
    print("[2] Opening login page...")
    driver.get("https://www.saucedemo.com/")

    print("[3] Entering username...")
    wait_for_element(driver, By.ID, "user-name").send_keys(USERNAME)

    print("[4] Entering password...")
    wait_for_element(driver, By.ID, "password").send_keys(PASSWORD)

    print("[5] Clicking login button...")
    wait_for_element(driver, By.ID, "login-button").click()

    print("[6] Login click completed.")


def validate_login(driver):
    print("[7] Validating login...")
    current_url = driver.current_url
    print(f"[DEBUG] Current URL after login: {current_url}")

    assert "inventory.html" in current_url, "Login failed: inventory page not reached."
    print("Login validation passed.")


def perform_actions(driver):
    print("[8] Adding product to cart...")
    wait_for_element(driver, By.ID, "add-to-cart-sauce-labs-backpack").click()

    print("[9] Opening cart...")
    wait_for_element(driver, By.CLASS_NAME, "shopping_cart_link").click()

    print("[10] Clicking checkout...")
    wait_for_element(driver, By.ID, "checkout").click()

    print("[11] Filling out checkout form...")
    wait_for_element(driver, By.ID, "first-name").send_keys(FIRST_NAME)
    wait_for_element(driver, By.ID, "last-name").send_keys(LAST_NAME)
    wait_for_element(driver, By.ID, "postal-code").send_keys(POSTAL_CODE)

    print("[12] Submitting checkout form...")
    wait_for_element(driver, By.ID, "continue").click()


def validate(driver):
    print("[13] Validating checkout overview page...")
    page_title = wait_for_element(driver, By.CLASS_NAME, "title").text
    print(f"[DEBUG] Page title found: {page_title}")

    assert page_title == "Checkout: Overview", f"Unexpected page title: {page_title}"
    print("Final validation passed.")


def close_browser(driver):
    print("[14] Closing browser...")
    driver.quit()


def main():
    driver = None

    try:
        driver = start_browser()
        login(driver)
        validate_login(driver)
        perform_actions(driver)
        validate(driver)
        print("Automation completed successfully.")

    except AssertionError as e:
        print(f"Validation error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        if driver:
            input("Press ENTER to close browser...")
            close_browser(driver)


if __name__ == "__main__":
    main()