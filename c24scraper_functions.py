
def Wait2Load(driver, timeout=2):
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    try:
        element_present = EC.presence_of_element_located((By.ID, 'c24-page-container-content'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded") # ensure that the page loads regularly
