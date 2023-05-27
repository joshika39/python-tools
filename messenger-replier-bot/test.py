from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import subprocess

def search_elements(tag: str, attribute: str, value: str):
    return browser.find_elements(By.XPATH, f"//{tag}[@{attribute}='{value}']")
          
        

def search_element_by_class(class_list: str, tag="*"):    
    test = browser.find_elements(By.CSS_SELECTOR, f"{tag}[class='{class_list}']")
    if len(test) > 0: 
        return test[0]
    
    return None
        

def click_button(attribute: str, value: str):
    for button in browser.find_elements(By.TAG_NAME, "button"):
        button_attr = button.get_attribute(attribute)
        if button_attr is not None and button_attr == value:
            button.click()


def get_text_box():
    msgDiv = search_elements("div", "aria-label", "Message")[0]
    while msgDiv is None:
        msgDiv = search_elements("div", "aria-label", "Message")[0]
    
    return msgDiv

def get_send_button():
    btn = search_elements("div", "aria-label", "Press enter to send")[0]
    while btn is None:
        btn = search_elements("div", "aria-label", "Press enter to send")[0]
    
    return btn

base_url = "https://www.facebook.com/messages/"
csenge = "100006367207301"

# passTxt = input("enter your password: ")
# email = "josh.hegedus@outlook.com"
# twoFa = input("Enter 2fa code: ")


email = subprocess.run(['bw', 'get', 'username', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 
passTxt = subprocess.run(['bw', 'get', 'password', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 
twoFa = subprocess.run(['bw', 'get', 'totp', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 

browser = webdriver.Edge()
browser.set_window_size(1500, 900)

browser.get(f'{base_url}t/{csenge}')

username = browser.find_element(By.ID, "email")
password = browser.find_element(By.ID, "pass")
submit   = browser.find_element(By.ID, "loginbutton")
username.send_keys(email)
password.send_keys(passTxt)

click_button("data-cookiebanner", 'accept_only_essential_button')

submit.click()

approvalCode = browser.find_element(By.ID, "approvals_code")
approvalCode.send_keys(twoFa)

test = browser.find_elements(By.ID, "checkpointSubmitButton")
while test and len(test) > 0:
    test[0].click()
    test = browser.find_elements(By.ID, "checkpointSubmitButton")


# message = get_text_box()
# message.send_keys("Test Msg")

# sendButton = search_element("div", "aria-label", "Press enter to send")
# sendButton.click()

unread_msg = search_elements("div", "aria-label", "Mark as read")

print(f"You have {len(unread_msg)} unread messages.")

for msg in unread_msg:
    msg.click()

finish = input("Enter anything to exit...")