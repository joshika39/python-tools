from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions

import subprocess

def search_element(driver: WebDriver, by: By, id: str):
    try:
        return driver.find_element(by, id)
    except:
        return None


def search_elements_by_xpath(driver: WebDriver, tag: str, attribute: str, value: str):
    return driver.find_elements(By.XPATH, f"//{tag}[@{attribute}='{value}']")
          

def search_elements_by_class(driver: WebDriver, class_list: str, tag="*"):    
    return driver.find_elements(By.CSS_SELECTOR, f"{tag}[class='{class_list}']")
        

def click_button(driver: WebDriver, attribute: str, value: str):
    for button in driver.find_elements(By.TAG_NAME, "button"):
        button_attr = button.get_attribute(attribute)
        if button_attr is not None and button_attr == value:
            button.click()


def get_text_box(driver: WebDriver):
    msgDiv = search_elements_by_xpath(driver, "div", "aria-label", "Message")[0]
    while msgDiv is None:
        msgDiv = search_elements_by_xpath(driver, "div", "aria-label", "Message")[0]
    
    return msgDiv

def get_send_button(driver: WebDriver):
    btn = search_elements_by_xpath(driver, "div", "aria-label", "Press enter to send")[0]
    while btn is None:
        btn = search_elements_by_xpath(driver, "div", "aria-label", "Press enter to send")[0]
    
    return btn


def chat_is_profile(driver: WebDriver, chat_id: str) -> bool:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(f'https://www.facebook.com/{chat_id}')

    results = search_elements_by_class(driver, "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xtoi2st x3x7a5m x1603h9y x1u7k74 x1xlr1w8 xi81zsa x2b8uid")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    if len(results) == 0:
        return True
    
    return False


def login(start_url: str, driver_options=Options()) -> WebDriver:
    driver = webdriver.Chrome(options=driver_options)
    # driver = webdriver.Remote('http://localhost:4444/wd/hub', options=Options())
    driver.maximize_window()

    
    driver.get(start_url)

    username = search_element(driver, By.ID, "email")
    if username is None:
        return driver
    password = search_element(driver, By.ID, "pass")
    submit   = search_element(driver, By.ID, "loginbutton")

    username.send_keys(email)
    password.send_keys(passTxt)

    click_button(driver, "data-cookiebanner", 'accept_only_essential_button')

    submit.click()

    approvalCode = driver.find_element(By.ID, "approvals_code")
    approvalCode.send_keys(twoFa)

    test = driver.find_elements(By.ID, "checkpointSubmitButton")
    while test and len(test) > 0:
        test[0].click()
        test = driver.find_elements(By.ID, "checkpointSubmitButton")
    
    return driver

base_url = "https://www.facebook.com/messages/"
csenge = "100006367207301"


# passTxt = input("enter your password: ")
# email = "josh.hegedus@outlook.com"
# twoFa = input("Enter 2fa code: ")


email = subprocess.run(['bw', 'get', 'username', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 
passTxt = subprocess.run(['bw', 'get', 'password', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 
twoFa = subprocess.run(['bw', 'get', 'totp', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 


browser = login(f'{base_url}t/{csenge}')

# browser = webdriver.Remote('http://localhost:4444/wd/hub', options=Options())
# browser.set_window_size(1500, 900)

# message = get_text_box()
# message.send_keys("Test Msg")

# sendButton = search_element("div", "aria-label", "Press enter to send")
# sendButton.click()

unread_msg = search_elements_by_xpath(browser, "div", "aria-label", "Mark as read")

try:
    unread_msg = WebDriverWait(browser, 10).until(
        expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Mark as read']")))
except:
    print(f"You have 0 unread messages.")
    
print(f"You have {len(unread_msg)} unread messages.")

chats = search_elements_by_class(browser, "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq xdj266r x11i5rnm xat24cr x1mh8g0r x1y1aw1k x1sxyh0 xwib8y2 xurb0ha")

print(f"You have {len(chats)} ongoing conversation")

for chat in chats:
    try:
        full_link = chat.get_attribute("href")
        id = full_link.replace('https://www.facebook.com/messages/t/', '')
        is_person = chat_is_profile(browser, id)
        if(is_person):
            child = chat.find_elements(By.XPATH, ".//div[@aria-label='Mark as read']")
            if len(child) > 0:
                print(f'{full_link} -> Person (Unread)')
            else:
                print(f'{full_link} -> Person (Read)')
        else:
            print(f'{full_link} -> Group (undefined)')
    except:
        print("Unhandled exception with chat crawling")

finish = input("Enter anything to exit...")
