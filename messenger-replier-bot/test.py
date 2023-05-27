from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def search_element(tag: str, attribute: str, value: str):
    for element in browser.find_elements(By.TAG_NAME, tag):
        element_attr = element.get_attribute(attribute)
        if element_attr is not None and element_attr == value:
            return element

def click_button(attribute: str, value: str):
    for button in browser.find_elements(By.TAG_NAME, "button"):
        button_attr = button.get_attribute(attribute)
        if button_attr is not None and button_attr == value:
            button.click()


passTxt = input("enter your password: ")
email = "josh.hegedus@outlook.com"
twoFa = input("Enter 2fa code: ")


browser = webdriver.Edge()

browser.get("https://www.facebook.com/messages/")

username = browser.find_element(By.ID, "email")
password = browser.find_element(By.ID, "pass")
submit   = browser.find_element(By.ID, "loginbutton")
username.send_keys(email)
password.send_keys(passTxt)

click_button("data-cookiebanner", 'accept_only_essential_button')

submit.click()

approvalCode = browser.find_element(By.ID, "approvals_code")
approvalCode.send_keys(twoFa)

while browser.find_element(By.ID, "checkpointSubmitButton") is not None:
    browser.find_element(By.ID, "checkpointSubmitButton").click()

msgDiv = search_element("div", "aria-label", "Message")
if msgDiv is not None:
    msgDiv.send_keys("Test Msg")

finish = input("Enter anything to exit...")