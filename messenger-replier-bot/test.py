from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

from json_service import JsonService
from base import curr_dir
import os
import subprocess


def get_basic_login() -> list[str]:
    email = subprocess.run(['bw', 'get', 'username', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 
    passTxt = subprocess.run(['bw', 'get', 'password', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8") 
    return [email, passTxt]

def get_totp() -> str:
    return subprocess.run(['bw', 'get', 'totp', 'f6280c44-154b-46f8-9e08-ad3b00c739da'], stdout=subprocess.PIPE).stdout.decode("utf-8")


users_path = os.path.join(curr_dir(), 'users.json')

def search_element(driver: WebDriver, by: By, id: str):
    try:
        return driver.find_element(by, id)
    except:
        return None


def search_elements_by_xpath(driver: WebDriver, tag: str, attribute: str, value: str):
    try:
        results = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.XPATH, f"//{tag}[@{attribute}='{value}']")))
        return results
    except:
        return []

def search_child_elements_by_xpath(parent: WebElement, tag: str, attribute: str, value: str):
    try:
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


def get_text_box(driver: WebDriver):
    msgDivs = search_elements_by_xpath(driver, "div", "aria-label", "Message")

    while len(msgDivs) == 0:
        msgDivs = search_elements_by_xpath(driver, "div", "aria-label", "Message")
    
    return msgDivs[0]

def get_send_button(driver: WebDriver):
    btn = search_elements_by_xpath(driver, "div", "aria-label", "Press enter to send")
    while len(btn) == 0:
        btn = search_elements_by_xpath(driver, "div", "aria-label", "Press enter to send")
    
    return btn[0]


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

def submit_approval(driver: WebDriver):
        try:
            approvalCode = driver.find_element(By.ID, "approvals_code")
            approvalCode.send_keys(get_totp())
        except:
            return

def login(start_url: str, driver_options=Options()) -> WebDriver:
    driver = webdriver.Chrome(options=driver_options)
    driver.maximize_window()   
    driver.get(start_url)

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
    
    return driver


def send_message(driver: WebDriver, target_id: str,message: str):
    driver.get(f'https://www.facebook.com/messages/t/{target_id}')
    messageBox = get_text_box(driver)
    messageBox.send_keys(message)
    sendButton = get_send_button(driver)
    sendButton.click()


def get_unread_chats(driver: WebDriver) -> list[WebElement]:
    
    chat_box = search_elements_by_class(driver, "x78zum5 xdt5ytf x1iyjqo2 x5yr21d x6ikm8r x10wlt62")[0]
    chat_box.location_once_scrolled_into_view

    chats = search_elements_by_class(driver, "x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq xdj266r x11i5rnm xat24cr x1mh8g0r x1y1aw1k x1sxyh0 xwib8y2 xurb0ha")
    print(f"You have {len(chats)} ongoing conversation")
    
    
    # driver.execute_script("arguments[0].scrollIntoView();", chats[-1])

    unread_chats = []  #type: list[WebElement]
    json_serice = JsonService(users_path)
    registered_users = json_serice.read("users")
    for chat in chats:
        try:
            full_link = chat.get_attribute("href")
            id = full_link.replace('https://www.facebook.com/messages/t/', '')[:-1]
            if id not in registered_users:
                is_person = chat_is_profile(driver, id)
                if is_person:
                    user = {"type" : "person"}
                    registered_users[id] = user
                else:
                    user = {"type" : "group"}
                    registered_users[id] = user
            else:
                user = registered_users[id]
            
            child = chat.find_elements(By.XPATH, ".//div[@aria-label='Mark as read']")
            if len(child) > 0:
                unread_chats.append(chat)
        except:
            print("Unhandled exception with chat crawling")
    json_serice.write("users", registered_users)

    for chat in chats[-8:]:
        hover = ActionChains(driver).move_to_element(chat)
        hover.perform()
        context_menu = search_child_elements_by_xpath(chat, "div", "aria-label", "Menu")
        context_menu[0].click()
        menu_items = search_elements_by_class(driver, "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou xe8uvvx x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct x9f619 x1ypdohk x78zum5 x1q0g3np x2lah0s xnqzcj9 x1gh759c xdj266r xat24cr x1344otq x1de53dj x1n2onr6 x16tdsg8 x1ja2u2z x6s0dn4 x1y1aw1k xwib8y2")
        if len(menu_items) > 5:
            menu_items[6].click()
        # input("check the browser")
    # if len(chats) > 10:
    #     chats_to_clear = len(chats) - 10
    #     targets = chats[-chats_to_clear:]
    #     for target in targets:
    #         hover = ActionChains(driver).move_to_element(target)
    #         hover.perform()
    #         input("check the browser")

    return unread_chats

base_url = "https://www.facebook.com/messages/"
csenge = "100006367207301"
hanna = "100019317438894"
me = "100012409636478"

# passTxt = input("enter your password: ")
# email = "josh.hegedus@outlook.com"
# twoFa = input("Enter 2fa code: ")

browser = login(f'{base_url}t/{me}')

# browser = webdriver.Remote('http://localhost:4444/wd/hub', options=Options())
# browser.set_window_size(1500, 900)

get_unread_chats(browser)

# send_message(browser, csenge, "Test Msg")
# send_message(browser, hanna, "Test Msg")

finish = input("Enter anything to exit...")


# unread_msg = search_elements_by_xpath(browser, "div", "aria-label", "Mark as read")
# try:
#     unread_msg = WebDriverWait(browser, 10).until(
#         expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Mark as read']")))
# except:
#     print(f"You have 0 unread messages.")
    
# print(f"You have {len(unread_msg)} unread messages.")
# print(f"You have {len(chats)} ongoing conversation")
