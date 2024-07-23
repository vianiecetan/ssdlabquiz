from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# URL of the Flask application
url = "http://localhost:8000"

# Test data
valid_search_term = "flask"
invalid_search_term = "<script>alert('xss');</script>"

@pytest.fixture
def browser():
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # You can use any other WebDriver like Firefox
    yield driver
    driver.quit()

def test_search_with_valid_term(browser):
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    
    # Wait until the home page is loaded
    wait.until(EC.title_contains("Home Page"))
    
    # Enter valid search term
    search_box = browser.find_element(By.NAME, "search_term")
    search_box.send_keys(valid_search_term)
    search_box.send_keys(Keys.RETURN)  # Submit the form
    
    # Check the result
    expected_title = "Result Page"
    assert wait.until(EC.title_contains(expected_title))
    
    # Verify that the search term is displayed on the result page
    result_text = browser.find_element(By.TAG_NAME, "p").text
    assert valid_search_term in result_text

def test_search_with_invalid_term(browser):
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    
    # Wait until the home page is loaded
    wait.until(EC.title_contains("Home Page"))
    
    # Enter invalid search term
    search_box = browser.find_element(By.NAME, "search_term")
    search_box.send_keys(invalid_search_term)
    search_box.send_keys(Keys.RETURN)  # Submit the form
    
    # Verify that the user is still on the home page with a flash message
    expected_title = "Home Page"
    assert wait.until(EC.title_contains(expected_title))
    
    # Check for the flash message
    flash_message = browser.find_element(By.XPATH, "//body").text
    assert "Please try again." in flash_message
