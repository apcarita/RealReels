import undetected_chromedriver as uc
import ssl
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import pyautogui

def Art2(lines):
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = uc.Chrome(executable_path='chromedriver', options=options)
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    with open('playwright/state.json', 'r') as file:
        cookies = json.load(file)

    # Goto the same URL   
    driver.implicitly_wait(0.5)
    driver.get('https://www.krea.ai/apps/image/realtime')

    # Set stored cookies to maintain the session
    for cookie in cookies:
        driver.add_cookie(cookie)
    #driver.get("https://bot.sannysoft.com/")
    #driver.get("https://nowsecure.nl")
    checkPopUp(driver)

def checkPopUp(driver):
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mb-auto")))
    except Exception as e:
        element = None
        print("No popup appeared. Continuing execution...")

    if element:
        print("\n Signing in... \n")
        element.click()
        signIn(driver)

def signIn(driver):
    #click sign in w/google
    emailName = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/form/div/input")))
    time.sleep(2.1)

    email_username = os.getenv('EMAIL_USERNAME')
    email_password = os.getenv('EMAIL_PASSWORD')    
    print(f"signing in using credentials for {email_username}...\n")
    typeHuman(driver,emailName, email_username)

    buttond = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/form/button")))
    time.sleep(2.1)
    clickHuman(driver, buttond)
    time.sleep(3.2)
    emailPass = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div/div/form/div[2]/input")))
    typeHuman(driver, emailPass, email_password)
    time.sleep(1.8)
    cloudFlair = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/div/div/div[1]/div/label/input")))
    clickHuman(driver,cloudFlair)



def moveMouse(driver, element):
    # Get the element's location and size
    element_rect = element.rect
    target_x, target_y = element_rect['x'], element_rect['y']
    width, height = element_rect['width'], element_rect['height']

    # Calculate center of the element if needed
    element_center_x = target_x + width / 2
    element_center_y = target_y + height / 2

    print(f'is on screen: {pyautogui.onScreen(element_center_x, element_center_y)}')
    print(f'clicking {element_center_x}, {element_center_y}')

    # Initialize the action chain
    actions = ActionChains(driver)

    # Make sure we're working with coordinates that are within the element
    pyautogui.moveTo(element_center_x, element_center_y, 1.7, pyautogui.easeInElastic)

# Ensure this `moveMouse` function is used instead of the previous one in your original codebase.

def typeHuman(driver, element, input_string):
    delay = random.uniform(0.5, 0.3)
    time.sleep(delay)
    clickHuman(driver, element)
    for char in input_string:
        # Random delay to simulate human typing speed
        delay = random.uniform(0.05, 0.3)
        time.sleep(delay)
        # Send each character to the element
        element.send_keys(char)
def clickHuman(driver, element):
    #moveMouse(driver, element)
    # Initialize the action chain
    actions = ActionChains(driver)
    # Move to the element and click with hold and release
    actions.move_to_element(element).click_and_hold(on_element=None).perform()
    # Random delay to simulate human hold time
    hold_time = random.uniform(0.1, 0.5)  # Hold the mouse button for 100ms to 500ms
    time.sleep(hold_time)
    # Release the mouse button
    actions.release(on_element=None).perform()
    # Additional small pause to simulate human reaction time
    time.sleep(random.uniform(0.05, 0.2))

def Art(lines):
    ssl._create_default_https_context = ssl._create_stdlib_context

    driver = uc.Chrome(
        use_subprocess=False,
    )

    # visit the target URL
    driver.get("https://bot.sannysoft.com/")

    # print the URL
    print(driver.current_url)  # https://www.hapag-lloyd.com/en/home.html

    # get the website's title
    print(driver.title)  # Hapag-Lloyd - Global container liner shipping - Hapag-Lloyd

    # close the browser
    driver.quit()





if __name__ == "__main__":
    Art2("In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep")
