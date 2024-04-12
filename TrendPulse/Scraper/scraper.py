from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from pipelines import TweetsClean
import json
import settings
from decouple import config

tweets_clean = TweetsClean()

service = webdriver.ChromeService(executable_path=settings.PATH_CHROMEDRIVER)
driver = webdriver.Chrome(service = service)
driver.get("https://twitter.com/i/flow/login")
driver.set_window_size(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
sleep(3)

username = driver.find_element(By.XPATH, "//input[@class='r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7']")
username.send_keys(config("USERNAME"))
sleep(3)

next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
next_button.click()
sleep(3)

password = driver.find_element(By.XPATH, "//input[@class='r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7']")
password.send_keys(config("PASSWORD"))
log_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")
log_button.click()
sleep(5)

search_box = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search_box.send_keys(settings.SUBJECT)
search_box.send_keys(Keys.ENTER)
sleep(3)

def readTweets():
    data = []
    counter = 0

    articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    sleep(settings.SCROLL_PAUSE_TIME)

    while counter < settings.QUANTITY_TWEETS:
        for article in articles:
            tweet = {
                "user_tag": driver.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text,
                "time_stamp": driver.find_element(By.XPATH, ".//time").get_attribute('datetime'),
                "tweet":driver.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text,
                "reply": driver.find_element(By.XPATH, ".//div[@data-testid='reply']").get_attribute('aria-label'),
                "retweet": driver.find_element(By.XPATH, ".//div[@data-testid='retweet']").get_attribute('aria-label'),
                "like": driver.find_element(By.XPATH, ".//div[@data-testid='like']").get_attribute('aria-label'),
                "visualizations": driver.find_element(By.XPATH, ".//a[@class='css-175oi2r r-1777fci r-bt1l66 r-bztko3 r-lrvibr r-1ny4l3l r-1loqt21']").get_attribute('aria-label')
            }
            dict_clean = tweets_clean.clean(tweet)
            its_here = tweets_clean.its_here(data, tweet["tweet"])
            if its_here == False:
                #print(dict_clean)
                data.append(dict_clean)
                counter = counter + 1

        driver.execute_script(settings.SCROLL_SCRIPT)
        sleep(settings.SCROLL_PAUSE_TIME)
        articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    return data

def save_json(data):
    with open(settings.NAME_FILE, "w") as file:
        json.dump(data, file, ensure_ascii=False)

save_json(readTweets())