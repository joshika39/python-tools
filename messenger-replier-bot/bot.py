from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
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
import time
from pyperclip import copy
msg_hu_list = [
    'Hello,',
    ' ',
    'Ezt az üzenetet egy automatikus üzenetrögzítő írja. '
    'Joshua 5 után lesz elérhető, megértésed köszöni. ',
    ' ',
    'Addig is, további szép napot! ',
    ' ',
    'English language switch is under development.',
    ' ',
    '-----BEGIN PGP PUBLIC KEY BLOCK-----',
    'mDMEZHSC/hYJKwYBBAHaRw8BAQdAQ4D+KzJ95Uk4qIEZMra8irFm9ekzzdExhb1c',
    'pvWjmPC0JEpvc2h1YSBIZWdlZHVzIDxqaGVnZWR1czlAZ21haWwuY29tPoiZBBMW',
    'CgBBFiEEiEMkR44cIFZNVs/KWBFXYvv8AsoFAmR0gv4CGwMFCQPCZwAFCwkIBwIC',
    'IgIGFQoJCAsCBBYCAwECHgcCF4AACgkQWBFXYvv8AsqyewEApzgWXRkKl6BPHf+/',
    'e3xQthB6d0Oq/hMaYT/zjLvPS7oA/11OkDCKR5TnVSbeLOH4fBpbhMhaDpFaBU0R',
    'lM1OVyIJuDgEZHSC/hIKKwYBBAGXVQEFAQEHQP2lrIHopA9i+nh62HKwGE23M7nD',
    'eJSbSruDl7q+k81ZAwEIB4h+BBgWCgAmFiEEiEMkR44cIFZNVs/KWBFXYvv8AsoF',
    'AmR0gv4CGwwFCQPCZwAACgkQWBFXYvv8AsrDngD+M0L4XtxUJS8xxFrxLyjDs11o',
    'gk5AoErQs1lz8qagDYwBAJK7jVQ5MzPYRZQ6BhnDFq0W2pZA0MMU32fVjvehbVcB',
    '=nZLD',
    '-----END PGP PUBLIC KEY BLOCK-----',
    ' ',
    '(Sent by an automated replier system.)',
    'Version: v0.0.1-alpha'
]

msg_en = """
Hello, 

Ez a joshuanaka az automatikus uzenet kezeloje.

Joshua majd 6 utan, tud valaszolni, koszonom a megertesed.

(Sent by an automated replier system.)
Version: 024723094897jsfw3r-08v923h932
"""
users_path = os.path.join(curr_dir(), 'users.json')

base_url = f"https://www.facebook.com/messages/t/{JsonService(users_path).read('people/csenge')}"


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


def search_elements_by_xpath(driver: WebDriver, tag: str, attribute: str, value: str) -> list[WebElement]:
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


def send_message(driver: WebDriver, target_id: str, messages: list[str]):
    sent = False
    tries = 4
    driver.get(f'https://www.facebook.com/messages/t/{target_id}')
    messageBox = search_elements_by_class(driver, "xat24cr xdj266r", "p")
    if len(messageBox) <= 0:
        print("Could get message box")
        return
    messageBox = messageBox[0]
    while not sent and tries >= 0:
        try:
            sent = True
            for message in messages:
                messageBox.send_keys(message + Keys.SHIFT + Keys.ENTER)
            messageBox.send_keys(Keys.ENTER)
            print(f"Message sent to: {target_id}")
        except Exception as e:
            sent = False
            print(f"Could not enter message: {e}")
        finally:
                tries -= 1
    driver.get(base_url)


def get_unread_chats(driver: WebDriver) -> dict:
    chats_str = "xurb0ha x1sxyh0 x1n2onr6" 
    chats = search_elements_by_class(driver, chats_str)

    unread_users = {}  #type: dict
    json_serice = JsonService(users_path)
    registered_users = json_serice.read("conversations")
    testers = json_serice.read("beta_testers")
    i = 0
    while i < len(chats):
        success = False
        chat = chats[i]
        try:
            if not chat.is_displayed():
                driver.execute_script("document.querySelector(div[class='x78zum5 xdt5ytf x1iyjqo2 x5yr21d x6ikm8r x10wlt62']).scrollTop=500")
            link_elem = search_child_elements_by_xpath(chat, 'a', 'role', 'link')[0]
            full_link = link_elem.get_attribute("href")
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
            
            child = search_child_elements_by_xpath(chat, 'div', 'aria-label', 'Mark as read')
            if len(child) > 0 and id in testers:
                unread_users[id] = user
            success = True
        except StaleElementReferenceException as e:
            print("Refreshing chats....")
            chats = search_elements_by_class(driver, chats_str)
            success = False
        except Exception as e:
            print(f"Unhandled exception with chat crawling: {e}")
        finally:
            if success:
                i += 1
    json_serice.write("conversations", registered_users)
    
    if len(chats) > 10:
        success = False
        old_chats = chats[-10:]
        i = 0
        while i < len(old_chats) and len(chats) > 10:
            chat = old_chats[-1]
            try:
                hover = ActionChains(driver).move_to_element(chat)
                hover.perform()
                context_menu = search_child_elements_by_xpath(chat, "div", "aria-label", "Menu")
                if len(context_menu) > 0:
                    context_menu[0].click()
                    menu_items = search_elements_by_class(driver, "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou xe8uvvx x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct x9f619 x1ypdohk x78zum5 x1q0g3np x2lah0s xnqzcj9 x1gh759c xdj266r xat24cr x1344otq x1de53dj x1n2onr6 x16tdsg8 x1ja2u2z x6s0dn4 x1y1aw1k xwib8y2")
                    if len(menu_items) == 9:
                        menu_items[6].click()
                    elif len(menu_items) == 8:
                        menu_items[4].click()
                    elif len(menu_items) == 3:
                        menu_items[1].click()
                else:
                    print("Context menu not found!")
            except StaleElementReferenceException as e:
                chats = search_elements_by_class(driver, chats_str)
                if len(chats) > 10:
                    old_chats = chats[-10:]
                success = False
            except Exception as e:
                success = False
                print(f"Could not open menu: {e}")
            finally:
                if success:
                    i += 1
    
    return unread_users


def get_nth_msg(driver: WebDriver, target: str, count: int):
    driver.get(f'https://www.facebook.com/messages/t/{target}')
    messages = search_elements_by_class(driver, "x6prxxf x1fc57z9 x1yc453h x126k92a xzsf02u", tag='div')
    # for message in messages:
    #     print(message.text)
    if len(messages) > 0 and messages[-1] == "en":
        send_message(driver, target, )




start = ""

option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)

browser = login(base_url, option)

# get_nth_msg(browser, "100015000309137", 3)

while True:
    time.sleep(2)
    unreads = get_unread_chats(browser)
    print(f"Current chages: {len(unreads)}")
    if len(unreads) > 0:
        for unread in unreads:
            if unreads[unread]['type'] == 'person':
                # print(f"Unread: {unread}")
                send_message(browser, unread, msg_hu_list)
