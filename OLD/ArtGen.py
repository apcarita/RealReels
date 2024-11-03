
from playwright.sync_api import sync_playwright, Playwright
import os

def setEnv():
    os.environ["SESSION_STORAGE"] = '{"ph_phc_kyzaz2uOZkTGjBpixpJPev9B8cusob2snVtgYXoIn96_primary_window_exists":"true","sveltekit:snapshot":"{}","sveltekit:scroll":"{\\"1729780122410\\":{\\"x\\":0,\\"y\\":1275.5},\\"1729780167861\\":{\\"x\\":0,\\"y\\":0}}","ph_phc_kyzaz2uOZkTGjBpixpJPev9B8cusob2snVtgYXoIn96_posthog":"{\\"$referrer\\":\\"$direct\\",\\"$referring_domain\\":\\"$direct\\"}","ph_phc_kyzaz2uOZkTGjBpixpJPev9B8cusob2snVtgYXoIn96_window_id":"\\"0192bf63-9173-7ce5-a944-41461508214e\\""}' 

def Art(lines):

    
    from playwright.sync_api import sync_playwright
    playwright = sync_playwright().start()
    # Use playwright.chromium, playwright.firefox or playwright.webkit
    # Pass headless=False to launch() to see the browser UI
    browser = playwright.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled', '--enable-webgl',
        '--use-gl=swiftshader',
        '--enable-accelerated-2d-canvas'])

    context =  browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        device_scale_factor=1,
        locale='en-US',
        timezone_id='America/New_York',
        storage_state="playwright/state.json"
        )

    page = context.new_page()
    print(context.storage_state)
  
    # Set session storage in a new context
    session_storage = '{"ph_phc_kyzaz2uOZkTGjBpixpJPev9B8cusob2snVtgYXoIn96_primary_window_exists":"true","sveltekit:snapshot":"{}","sveltekit:scroll":"{\\"1729780122410\\":{\\"x\\":0,\\"y\\":1275.5},\\"1729780167861\\":{\\"x\\":0,\\"y\\":0}}","ph_phc_kyzaz2uOZkTGjBpixpJPev9B8cusob2snVtgYXoIn96_posthog":"{\\"$referrer\\":\\"$direct\\",\\"$referring_domain\\":\\"$direct\\"}","ph_phc_kyzaz2uOZkTGjBpixpJPev9B8cusob2snVtgYXoIn96_window_id":"\\"0192bf63-9173-7ce5-a944-41461508214e\\""}'
    print(session_storage)

    context.add_init_script("""(storage => {
        const entries = JSON.parse(storage)
        for (const [key, value] of Object.entries(entries)) {
        window.sessionStorage.setItem(key, value)
    }
    })('""" + session_storage + "')")
    

    page.goto("https://www.krea.ai/apps/image/realtime")

    page.wait_for_timeout(332)

    page.get_by_role("button", name="Text").click()

    promt = page.locator("#prompt")
    promt.click()
    promt.press('Control+a')
    promt.press('Delete')
    promt.press_sequentially(lines)

    page.get_by_label("img").screenshot(path="example.png")
    page.pause()
    browser.close()
    playwright.stop()

if __name__ == "__main__":
    Art("In the beginning God created the heaven and the earth. And the earth was without form, and void; and darkness was upon the face of the deep")