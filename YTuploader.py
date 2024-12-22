
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
COOKIE_FILE_NAME = "cookies/.session.dat"

async def upload(videos, texts, hashtags, channel):
    retries = 4
    driver = await uc.start()
    for attempt in range(retries):
        try:
            tab = await driver.get("https://studio.youtube.com/channel/UCxUs1VPVupc6-aPa7Pxl97w/videos/upload?")
            # Check if the page loaded correctly by looking for a specific element
            check = tab.select("#contentIcon > tp-yt-iron-icon")
            print(check)
            check2 = tab.select("#headingText > span")
            if await check or check2:
                print("Page loaded successfully.")
                break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                print("Failed to load the page after multiple attempts.")
                return
            await driver.sleep(1)  # Wait before retrying

    print("attepting to laod cookies")
    await load_cookies(driver, tab)

    while True:
        current_url = await tab.get_url()
        print(current_url)
        if "accounts.google.com" in current_url:
            await asyncio.sleep(1)
            print("please log in... manually")
        else:
            await save_cookies(driver)
            print("logged and saved cookies sucessfully")
            break

    await tab.sleep(1)
    current_url = await tab.get_url()

    if("signin_prompt" in current_url):
        channelSelect = await tab.find_element_by_text("Dont Scroll If You Love Jesus")
        await channelSelect.click()
    if(await tab.select("#dialog")):
        cookioes = await tab.select("#dialog")
        await cookioes.click()

    clickt(tab, "button.px-3:nth-child(2)")
async def save_cookies(browser):
    try:
        await browser.cookies.save(COOKIE_FILE_NAME)
        print("Cookies saved.")
    except Exception as e:
        print(f"Failed to save cookies: {e}")

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

async def clickt(tab, selector):
    await tab.select(selector)
    await tab.click()  
    await tab.sleep(random.uniform(0.25, 1))

if __name__ == "__main__":
    asyncio.run(upload("/Users/adam/Documents/COde/RelReels/Generated_Genesis/Final/Genesis 7:[23-25].mp4", "Genesis 7:[23-25]", "And every living substance was destroyed which was upon the face of", "Dont Scroll If You Love Jesus"))
