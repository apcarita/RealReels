import asyncio
import random
import string
import logging
from dotenv import load_dotenv
import json
from SafeSearch import detect_safe_search

logging.basicConfig(level=30)

try:
    import nodriver as uc
except (ModuleNotFoundError, ImportError):
    import sys, os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import nodriver as uc
import os

load_dotenv()

USER = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
COOKIE_FILE_NAME = ".session.dat"


async def fetchArt(line, chars_per_line, output_path):
    words = line.split(' ')
    driver = await uc.start()
    await asyncio.sleep(0.5)
    retries = 3
    tab = await driver.get("https://www.krea.ai/apps/image/realtime")

    while retries > 0:
        await tab.wait()
        print(tab.target.url)
        if tab.target.url != 'https://www.krea.ai/apps/image/realtime':
            tab = await driver.get("https://www.krea.ai/apps/image/realtime")
            await tab.wait(0.5)
        else:
            retries = -1
            break
        retries -= 1  
        if(retries == 0):
            driver = await uc.start()
            retries = 3 
            print("New Driver Started!")       
        print("Retrying... Attmept: ", 12- retries)
    print("Signing in...")
    await tab.set_window_size(0, 0, 1928, 1317)

    
    if not await load_cookies(driver, tab) or "hi" == "Sign Up":
        print("Please log in manually.")
        await tab.sleep(40)  # Give the user 60 seconds to log in manually

        tab = await driver.get("https://www.krea.ai/apps/image/realtime")
        await save_cookies(driver)
        print("Cookeis Saved!")
    else:
        print("Logged in with cookies.")
    await tab.sleep(3)

    #Click to enter text mode
    text_button = await tab.select("button.px-3:nth-child(2)")
    await text_button.click()
    scale_button = await tab.find("1:1", best_match=True)
    await scale_button.click()
    await scale_button.click()

    text_area = await tab.select("textarea")
    await text_area.click()
    image_area = await tab.select("img.rounded-md")
    # Clear input
    await text_area.clear_input()
    await text_area.clear_input()

    images = []
    
    text = ' '.join(words)
    pretext = text[:35]
    text = text[35:]
    await tab.scroll_down(20)
    #await tab.scroll_down(30)

    image_count = 1

    await text_area.send_keys(pretext)
    await tab.sleep(2)

    for i in range(0, len(text), chars_per_line):
        snippet = text[i:i+chars_per_line]
        await text_area.send_keys(snippet)
        await tab.sleep(2)
        img_url = image_area.attrs.get("src")
        #print(f"Image URL: {img_url}")  # Debugging statement

        path = f"{output_path}/generate_{image_count}.jpg"
        print(f"typing: {snippet}... Saving to: {path}")
        await image_area.save_screenshot(path)
        #await tab.download_file(img_url, path)
        if(image_count == 1 or image_count == 2 or image_count == 3 or image_count == 4 or image_count == 10 or image_count == 15):
            if(detect_safe_search(path) ):
                raise ValueError("NSFW content detected. Aborting.")
                return None
        images.append(path)
        image_count += 1
    await tab.sleep(1)

    return images
    # Type our own text


async def type_text(element, text):
    for char in text:
        await element.send_keys(char)

async def login_with_credentials(page):
    email_field = await page.select("input[name=a_nick]")
    password_field = await page.select("input[name=a_pass]")

    if not email_field or not password_field:
        return False

    print("Logging in with credentials...")
    await type_text(email_field, USER)
    await type_text(password_field, PASSWORD)

    login_button = await page.select("input[type=submit]")
    if login_button:
        await login_button.click()
        return True

    return False

async def load_cookies(browser, page):
    try:
        await browser.cookies.load(COOKIE_FILE_NAME)
        await page.reload()
        print("Cookies loaded.")
        return True
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Failed to load cookies: {e}")
    except FileNotFoundError:
        print("Cookie file does not exist.")

    return False

async def save_cookies(browser):
    try:
        await browser.cookies.save(COOKIE_FILE_NAME)
        print("Cookies saved.")
    except Exception as e:
        print(f"Failed to save cookies: {e}")
async def login():
    driver = await uc.start()
    tab = await driver.get("https://www.krea.ai/apps/image/realtime")
    print("Please log in manually.")

    
    await tab.sleep(65)  # Give the user 60 seconds to log in manually
    await save_cookies(driver)
    print("Cookeis Saved!")
    

if __name__ == "__main__":
   uc.loop().run_until_complete(login())


