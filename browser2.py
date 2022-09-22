from dotenv import load_dotenv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
chrome_options = Options()
load_dotenv()
IG_USERNAME=os.getenv('IG_USERNAME')
IG_PASSWORD=os.getenv('IG_PASSWORD')
chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--window-size=200,900")
chrome_options.add_argument("--window-position=0,0")
chrome_options.add_argument("--auto-open-devtools-for-tabs")
chrome_options.user_data_dir = r"C:\Users\Peql\AppData\Local\Google\Chrome\User Data\Profile 4"
chrome_options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.136 Mobile Safari/537.36"
}
if __name__ == "__main__":
    initial_scroll = 300
    scroll_distance = 300
    driver = uc.Chrome(options=chrome_options)
    ac = ActionChains(driver)
    with open('usernames.txt','r+') as f:
        usernames = f.readlines()
        for username in usernames:
            username = username.strip()
            driver.get(f'https://www.instagram.com/{username}/feed')
            time.sleep(2000)
            for x in range(5):
                if x != 0:
                    print('NO')
                    driver.execute_script(f"window.scrollTo(window.pageYOffset, window.pageYOffset+(window.pageYOffset+{scroll_distance}))")
                    time.sleep(0.2)
                time.sleep(5)
                buttons = driver.find_elements(By.XPATH, '//button')
                i=0
                for button in buttons:
                    try:
                        if button.text == "":
                            button_html = button.get_attribute('innerHTML')
                            if "More Options" in button_html:
                                button.send_keys(Keys.RETURN)
                                time.sleep(0.3)
                                option_btns = driver.find_elements(By.XPATH, '//button[normalize-space()="Embed"]')
                                for option_btn in option_btns:
                                    option_btn.send_keys(Keys.RETURN)
                                    time.sleep(0.3)
                                    textareas = driver.find_elements(By.XPATH, '//textarea')
                                    for textarea in textareas:
                                        with open(f"{username}_feed.html",'a+',encoding="utf-8") as f:
                                            html_output = "<div class='igitem'>"
                                            html_output += textarea.text
                                            f.write(html_output)
                                        time.sleep(1.6)
                                        copy_btns = driver.find_elements(By.XPATH, '//button')
                                        for copy_btn in copy_btns:
                                            if copy_btn.text == "Copy Embed Code":
                                                copy_btn.send_keys(Keys.ESCAPE)
                                time.sleep(0.3)
                                i+=1
                                time.sleep(0.3)
                    except Exception as e:
                        print(e)
                        pass
                    