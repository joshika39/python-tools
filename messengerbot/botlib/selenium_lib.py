from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess

def get_basic_login() -> list[str]:
    email = subprocess.run(['bw', 'get', 'username', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8")
    passTxt = subprocess.run(['bw', 'get', 'password', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return [email, passTxt]

def get_totp() -> str:
    return subprocess.run(['bw', 'get', 'totp', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8")

def search_element(driver: WebDriver, by: By, id: str):
    try:
        return driver.find_element(by, id)
    except:
        return None


def search_elements_by_xpath(driver: WebDriver, args: list[str]) -> list[WebElement]:
    if len(args) != 3:
        return []
    try:
        tag = args[0]
        attribute = args[1]
        value = args[2]
        results = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, f"//{tag}[@{attribute}='{value}']")))
        return results
    except:
        return []

def search_child_elements_by_xpath(parent: WebElement, args: list[str]):
    """ Use as follows: [tag, attribute, value] """
    if len(args) != 3:
        return []
    try:
        tag = args[0]
        attribute = args[1]
        value = args[2]
        results = parent.find_elements(By.XPATH, f".//{tag}[@{attribute}='{value}']")
        return results
    except:
        return []
          

def search_elements_by_class(driver: WebDriver, class_list: str, tag="*") -> list[WebElement]: 
    try:
        results = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, f"{tag}[class='{class_list}']")))
        return results
    except:
        return []
    

def search_child_elements_by_class(parent: WebElement, class_list: str, tag="*") -> list[WebElement]: 
    try:
        results = parent.find_elements(By.CSS_SELECTOR, f"{tag}[class='{class_list}']")
        return results
    except:
        return []


def search_element_by_id(driver: WebDriver, element_id: str) -> WebElement: 
    try:
        result = WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.ID, element_id)))
        return result
    except:
        return None

def click_button(driver: WebDriver, attribute: str, value: str):
    for button in driver.find_elements(By.TAG_NAME, "button"):
        button_attr = button.get_attribute(attribute)
        if button_attr is not None and button_attr == value:
            button.click()


def submit_approval(driver: WebDriver):
        try:
            approvalCode = driver.find_element(By.ID, "approvals_code")
            approvalCode.send_keys(get_totp())
        except:
            return


def create_local(driver_options=Options()) -> WebDriver:
    return webdriver.Chrome(options=driver_options)


def connect_to_container(url: str, driver_options=Options()) -> WebDriver:
    driver = webdriver.Remote(url, desired_capabilities=DesiredCapabilities.CHROME, options=driver_options)
    return driver


def login(start_url: str, driver: WebDriver, bypass_login=False) -> WebDriver:
    driver.get(start_url)
    if bypass_login:
        return driver
    
    username = search_element(driver, By.ID, "email")
    if username is None:
        return driver
    password = search_element(driver, By.ID, "pass")
    submit   = search_element(driver, By.ID, "loginbutton")

    basic = get_basic_login()
    username.send_keys(basic[0])
    password.send_keys(basic[1])

    click_button(driver, "data-cookiebanner", 'accept_only_essential_button')
    submit.click()
    test = search_element_by_id(driver, "checkpointSubmitButton")
    while test is not None:     
        submit_approval(driver)
        test.click()
        test = search_element_by_id(driver, "checkpointSubmitButton")

    has_error = search_element_by_id(driver, "back")
    
    if has_error is not None:
        driver.get(start_url)
    
    return driver


def get_id_from_link(element: WebElement):
    try:
        link = element.get_attribute("href")
        if "messages/t" in link:
            return True, link.replace("https://www.facebook.com/messages/t/", "")[:-1]
        else:
            return False, ""
    except Exception: 
        print(f"error getting the link for: {element.text}")
        return False, ""
