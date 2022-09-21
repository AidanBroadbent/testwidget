from dotenv import load_dotenv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
load_dotenv()
IG_USERNAME=os.getenv('IG_USERNAME')
IG_PASSWORD=os.getenv('IG_PASSWORD')
chrome_options = uc.ChromeOptions()
chrome_options.user_data_dir = r"C:\Users\Peql\AppData\Local\Google\Chrome\User Data\Profile 4"
chrome_options.add_experimental_option('prefs', {
    'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})

def get_links(driver,username):
    for i in range(30):
        driver.execute_script(f"window.scrollTo({1+(i*400)}, {400+(i*400)})")
        time.sleep(0.6)
    time.sleep(3)
    links = driver.find_elements(By.XPATH, "//a[@role='link']")
    resolved_links = []
    for link in links:
        link_html = link.get_attribute('innerHTML')
        link_href = f"{link.get_attribute('href')}"
        if "<img" in link_html:
            resolved_links.append(link_href)
        old_links = []
        with open(f"links_{username}.txt","r+") as f:
            for line in f.readlines():
                old_links.append(line.strip())
        i=0
        for resolved_link in resolved_links:
            if f"{resolved_link}\n" in old_links:
                resolved_links.pop(i)
            i+=1
        print(resolved_links)
        with open(f"links_{username}.txt","w+") as f:
            for resolved_link in resolved_links:
                f.write(f"{resolved_link}\n")
            for old_link in old_links:
                f.write(f"{old_link}\n")
    return resolved_links[::-1]


def get_images(driver, ac, links):
    html_output = "<!DOCTYPE html><html><head></head><body>"
    html_output+= '<div class="ig-feed">'
    for link_string in links:
        driver.get(link_string)
        time.sleep(4)
        btns = driver.find_elements(By.XPATH, "//button[@type='button']")
        for btn in btns:
            btn_html = btn.get_attribute('innerHTML')
            if "More Options" in btn_html:
                btn.click()
                time.sleep(4)
                option_btns = driver.find_elements(By.XPATH, '//button[normalize-space()="Embed"]')
                for option_btn in option_btns:
                    option_btn.click()
                    time.sleep(4)
                    textareas = driver.find_elements(By.XPATH, '//textarea')
                    for textarea in textareas:
                        html_output+='<div class="ig-item">'
                        html_output+=textarea.text
                        html_output+='</div>'
        time.sleep(4)
    html_output+='</div>'
    html_output+='</body></html>'
    with open(f"{username}-feed.html","w+",encoding="utf-8") as f:
        f.write(html_output)

if __name__ == "__main__":
    driver = uc.Chrome(options=chrome_options)
    ac = ActionChains(driver)
    with open('usernames.txt','r+') as f:
        usernames = f.readlines()
        for username in usernames:
            username = username.strip()
            driver.get(f'https://www.instagram.com/{username}/')
            time.sleep(4)
            links = get_links(driver, username)
            get_images(driver, ac, links)