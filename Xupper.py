import asyncio
import random
import string
import logging
from dotenv import load_dotenv
import json
from pathlib import Path

logging.basicConfig(level=30)

try:
    from nodriver import *
except (ModuleNotFoundError, ImportError):
    import sys, os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from nodriver import *
import os
import sys
load_dotenv()


USER = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
COOKIE_FILE_NAME = ".Xsession.dat"

async def postX(file, title):
    driver = await start()
    await asyncio.sleep(0.5)
    retries = 2
    tab = await driver.get("https://x.com/compose/post")

    while retries > 0:
        await tab.wait()
        print(tab.target.url)
        if tab.target.url != 'https://x.com/compose/post' or tab.target.url == 'https://x.com/i/flow/login?redirect_after_login=%2Fcompose%2Fpost':
            tab = await driver.get("https://x.com/compose/post")
        else:
            retries = -1
            break
        retries -= 1  
        if(retries == 0):
            driver.stop()
            driver = await start()
            retries = 3 
            print("New Driver Started!")       
        print("Retrying... Attmept: ", 12- retries)
    print("Signing in...")

    cooked = await load_cookies(driver, tab)
 
    print("waiting  7 secods")
    await tab.sleep(7)  
    await tab.update_target()
    print(tab.target.url)
    print(tab.target.title)

    if tab.target.url != "https://x.com/compose/post":
        print("Cookies not loaded. Please sign in")
        timeout_count = 0
        print(timeout_count)
        while timeout_count/2 < 100:
            await tab.update_target()
            await tab.sleep(0.5)  
            timeout_count += 1
            print(timeout_count)
            if tab.target.url == "https://x.com/home":
                break
            print("Waiting for Login...")

        await tab.sleep(0.5)  

        await save_cookies(driver)
        print("Cookeis Saved!")

        await tab.sleep(2)  

        postButton = await tab.find("Post", True)
        await postButton.click()

    path = Path(file).resolve()
    file_input = await tab.select("input[type=file]")

    await tab.sleep(0.5)  
    print(tab.target.url)

    titleinput = await tab.select("div[contenteditable='true']")
    await type_text(titleinput, title)

    await file_input.send_file(path)

    await tab.sleep(20)  

    #wait for the thing to upload

    nextButton = await tab.select("button[data-testid='tweetButton']")
    await nextButton.click()
    await tab.sleep(1)  

    return True

async def type_text(element, text):
    for char in text:
        await element.send_keys(char)

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

async def uploadDir(intital_path, finsihsed_path):
    to_upload_dir = Path(intital_path)
    uploaded_dir = Path(finsihsed_path)
    uploaded_dir.mkdir(exist_ok=True)
    video_files = to_upload_dir.glob("*.mp4")

    for video_file in video_files:
        title = video_file.stem  # Use the file name (without extension) as the title
        success = await postX(str(video_file), title)
        if success:
            video_file.rename(uploaded_dir / video_file.name)
    

    if __name__ == "__main__":
        if len(sys.argv) != 3:
            print("Usage: python Xupper.py <initial_path> <finished_path>")
            sys.exit(1)

        initial_path = sys.argv[1]
        finished_path = sys.argv[2]

        asyncio.run(uploadDir(initial_path, finished_path))




