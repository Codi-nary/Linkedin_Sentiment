from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import keyring
import nltk



# link to browser and login
def browser_get_login(link, username, password ,driver):
    driver.get(link)
    time.sleep(2)
    elementID = driver.find_element(By.ID, 'session_key')
    elementID.send_keys(username)
    time.sleep(2)
    passwordID = driver.find_element(By.ID, 'session_password')
    passwordID.send_keys(password)
    time.sleep(2)
    return elementID.submit()


def retrieve(container):
    df = pd.DataFrame(data=None, columns=['Id', 'Post'])
    for post in container:
        df = df.append({'Id': post.id, 'Post': post.accessible_name}, ignore_index=True)

    return df


def container_remove(container):
    while len(container) != 0:
        for item in container:
            container.remove(item)

    return container


def linkedin_scraper():
    # login details
    username = 'navinjain9616@gmail.com'

    # keyring.set_password('linkedin')
    # get path to the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    browser_get_login('https://www.linkedin.com', 'navinjain9616@gmail.com',
                      keyring.get_password('linkedin', username), driver)
    linkedin_post = pd.DataFrame()

    while len(linkedin_post) <= 500:
        posts_container = driver.find_elements(By.CLASS_NAME, 'feed-shared-update-v2__description-wrapper')

        linkedin_post = retrieve(posts_container)

        driver.execute_script("window.scrollBy(0,5000)")

        posts_container = container_remove(posts_container)

    return linkedin_post


def main():
    #linkedin_scraper().to_excel('/Users/navin.jain/Desktop/Linkedin Sentiment/scraping_test.xlsx', index=False)
    linkedin_scraper()


if __name__ == "__main__":
    main()
