from dotenv import load_dotenv
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import urllib.request
import base64
import shutil
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
            print(username)
            try:
                os.mkdir(username)
            except:
                shutil.rmtree(f'{username}')
                os.mkdir(username)
            driver.get(f'https://www.instagram.com/{username}/feed')
            time.sleep(1)
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.SPACE)
            time.sleep(6)
            current = 0
            for q in range(3):
                articles = driver.find_elements(By.TAG_NAME, "article")
                for article in articles:
                    time.sleep(0.1)
                    print(f'POST: {current}')
                    imgs = article.find_elements(By.TAG_NAME,'img')
                    if imgs!=None:
                        img_num = 0
                        for img in imgs:
                            srcset = img.get_attribute('srcset')
                            if srcset == "":
                                continue
                            else:
                                srcset = srcset.split(',')
                                for src in srcset:
                                    if "1080w" in src:
                                        src = src.split(' 1080w')[0]
                                        urllib.request.urlretrieve(src, f"{username}/{current}-{img_num}.jpg")
                                        img_num+=1
                        print(f"IMAGES: {img_num}")
                    videos = article.find_elements(By.TAG_NAME, 'video')
                    if videos!=None:
                        video_num=0
                        for video in videos:
                            print(video)
                            video_src = video.get_attribute('src')
                            print(video_src)
                            if video_src != "" and "blob" not in video_src:
                                video_type = ".mp4"
                                if ".mov" in video_src:
                                    video_type = ".mov"
                                elif ".gif" in video_src:
                                    video_type = ".gif"
                                urllib.request.urlretrieve(video_src, f"{username}/{current}-{video_num}{video_type}")
                                video_num+=1
                            elif video_src != "" and "blob" in video_src:
                                poster_src = video.get_attribute('poster')
                                time.sleep(1)
                                urllib.request.urlretrieve(poster_src, f"{username}/{current}-preview-{video_num}.jpg")
                                video_num+=1
                        print(f"VIDEOS: {video_num}")
                    links = article.find_elements(By.TAG_NAME,'a')
                    for link in links:
                        link_text = link.get_attribute('href')
                        if "liked_by" in link_text:
                            post_url = link_text.split('liked_by')[0]
                            with open(f"{username}/{current}.txt","w+") as f:
                                f.write(post_url)
                            print(f"POST LINK: {link_text}")
                            break
                        elif "comment" in link_text:
                            post_url = link_text.split('comment')[0]
                            with open(f"{username}/{current}.txt","w+") as f:
                                f.write(post_url)
                            print(f"POST LINK: {link_text}")
                            break
                    current+=1
                    time.sleep(1)
                body = driver.find_element(By.XPATH,'//body')
                for z in range(8):
                    body.send_keys(Keys.SPACE)
                    time.sleep(0.5)
                time.sleep(7)
               
            
            # for t in range(50):
            #     body.send_keys(Keys.SPACE)
            #     time.sleep(0.1)
            # time.sleep(1)    
            # for header in headers:
            #     print(header)
            # for x in range(15):
            #     ac.move_to_element(header).click().perform()
            #     time.sleep(0.3) 
            #     ac.send_keys(Keys.SPACE)
            #     time.sleep(0.3) 
                    