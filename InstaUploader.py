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
load_dotenv()


USER = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
COOKIE_FILE_NAME = ".session.dat"

async def postReel(file, title):
    driver = await start()
    await asyncio.sleep(0.5)
    retries = 3
    tab = await driver.get("http://instagram.com/")

    while retries > 0:
        await tab.wait()
        print(tab.target.url)
        if tab.target.url != 'https://www.instagram.com/':
            tab = await driver.get("http://instagram.com/")
            await tab.wait(0.5)
        else:
            retries = -1
            break
        retries -= 1  
        if(retries == 0):
            driver = await start()
            retries = 3 
            print("New Driver Started!")       
        print("Retrying... Attmept: ", 12- retries)
    print("Signing in...")

    cooked = await load_cookies(driver, tab)
 
    try:
        postButton = await tab.find("Create", True)
        await postButton.click()

        await (await tab.find("Post", True)).click()

        path = Path(file).resolve()
        file_input = await tab.select("input[type=file]")
    except:
        print("Cookies not loaded. time to sign in")

        print("Baking fresh cookies!")
        emailField = await tab.select("#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > label > input")
        await type_text(emailField, USER)
    
        passwordField = await tab.select("#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(2) > div > label > input")
        await type_text(passwordField, PASSWORD)

        logInButton = await tab.select("#loginForm > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xqui205.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(3) > button > div")
        await logInButton.click()

        savePword = await tab.find("Save info", True)
        await savePword.click()

        await tab.sleep(4)

        await save_cookies(driver)
        print("Cookeis Saved!")

        tab.sleep(2)

        postButton = await tab.find("Create", True)
        await postButton.click()

        await (await tab.find("Post", True)).click()

        path = Path(file).resolve()
        file_input = await tab.select("input[type=file]")

    await tab.sleep(0.5)

    await file_input.send_file(path)

    await tab.sleep(4)

    nextButton = await tab.find("Next", True)
    await nextButton.click()
    await tab.sleep(1)
    
    nextButton = await tab.find("Next", True)
    await nextButton.click()
    
    await tab.sleep(1)

    textField = await tab.select("div[contenteditable='true']")
    await textField.click()
    await type_text(textField, title)

    await tab.sleep(1)

    shareButton = await tab.find("Share", True)
    await shareButton.click()

    await tab.sleep(30)
    print("Posted Reel!")

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
        success = await postReel(str(video_file), title)
        if success:
            video_file.rename(uploaded_dir / video_file.name)


