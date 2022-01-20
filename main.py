from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import random
import pickle
from auth_data import username, password

service = Service(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-notifications')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.headless = True

driver = webdriver.Chrome(
    service=service,
    options=options
)
driver.get('https://twitter.com/')
for cookie in pickle.load(open(f'{username}_cookies', 'rb')):
    driver.add_cookie(cookie)
time.sleep(2)
driver.refresh()
print('Run')


def xpath_exists(url):
    try:
        driver.find_element(By.XPATH, url)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist


def element_exists(element, url):
    try:
        element.find_element(By.XPATH, url)
        exist = True
    except NoSuchElementException:
        exist = False
    return exist



# def login(username=1, password=1):
#     try:
        # driver.get('https://twitter.com/i/flow/login')
        # time.sleep(7)
        #
        # username_input1 = driver.find_element(By.CLASS_NAME, 'r-30o5oe')
        # print(username_input1)
        # # driver.find_element_by_xpath('//a[@href="'+url+'"]')
        #
        # # username_input = driver.find_element(By.ID, 'email')
        # username_input1.clear()
        # username_input1.send_keys(username)
        # time.sleep(2)
        #
        # next_btn = driver.find_element\
        #     (By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]/div')
        # next_btn.click()
        # time.sleep(4)
        #
        # username_input2 = driver.find_element\
        #     (By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        # username_input2.clear()
        # username_input2.send_keys('@SuperPu67111519')
        # time.sleep(3)
        #
        # login_btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div')
        # login_btn.click()
        # time.sleep(3)
        #
        #
        # if xpath_exists('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input'):
        #     password_input = driver.find_element\
        #         (By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input')
        #     password_input.clear()
        #     password_input.send_keys(password)
        #     time.sleep(3)
        # else:
        #     password_input2 = driver.find_element\
        #         (By.XPATH,
        #     '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input')
        #     password_input2.send_keys(password)
        #     time.sleep(3)
        #
        # login_btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div')
        # login_btn.click()
        # time.sleep(4)
        #
        # pickle.dump(driver.get_cookies(), open(f'{username}_cookies', 'wb'))
        #
        # time.sleep(4)
    # except Exception as e:
    #     print(e)
# -----------------------------------------------------------


def retweet_new_tweet():
    try:
        driver.get('https://twitter.com/')
        time.sleep(5)
        articles = driver.find_elements(By.TAG_NAME, 'article')

        with open('list.txt', 'r', encoding='UTF-8-sig') as file:
            old_urls = file.read().splitlines()

        for n in range(0, len(articles)):
            if element_exists(articles[n], './/a[@href="/ru_rbc"]'):
                tweet_url = articles[n].find_element(By.XPATH, './/a[contains(@href, "status")]').get_attribute("href")
                if tweet_url not in old_urls:
                    print('new url: ', tweet_url)
                    articles = driver.find_elements(By.TAG_NAME, 'article')
                    print('art: ', articles)
                    print('art-n: ', articles[n])
                    print('art-url: ', tweet_url)

                    if element_exists(articles[n], './/div[@data-testid="retweet"]'):
                        articles[n].find_element(By.XPATH, './/div[@data-testid="retweet"]').click()
                        time.sleep(1)
                        articles[n].find_element(By.XPATH, '//span[text()="Retweet"]').click()
                        time.sleep(2)
                        with open('list.txt', 'a', encoding='UTF-8-sig') as file:
                            file.write(tweet_url + '\n')
                        print('Zapisal: ', tweet_url)
        print('Zakonchil')
    except Exception as e:
        print(e)
    except NoSuchElementException as e:
        print(e)


def reply_to_message():
    print('startmessage()')
    driver.get('https://twitter.com/')
    time.sleep(5)

    all_messages = driver.find_element(By.XPATH, '//a[@href="/messages"]').click()
    time.sleep(2)

    # for new message request
    if xpath_exists('//a[@href="/messages/requests"]'):
        driver.find_element(By.XPATH, '//a[@href="/messages/requests"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//div/div/span/span[contains(text(), "Accept")]').click()
        time.sleep(2)
        input_msg = driver.find_element(By.XPATH, '//div[contains(@class, "public-DraftStyleDefault-block")]/span').send_keys("Nice")
        send_btn = driver.find_element(By.XPATH, '//div[@aria-label="Send"]').click()

    conversations = driver.find_elements(By.XPATH, '//div[@data-testid="conversation"]')
    time.sleep(2)

    # for unread conversation
    for n in range(0, len(conversations)):
        conversations = driver.find_elements(By.XPATH, '//div[@data-testid="conversation"]')
        print('n=', n, ' ', conversations[n].value_of_css_property('background-color'))
        if conversations[n].value_of_css_property('background-color') != 'rgba(255, 255, 255, 1)':
            conversations[n].click()
            time.sleep(2)
            # message_text = driver.find_element(By.XPATH, '//div[@role="presentation"]/div/span').text
            input_msg = driver.find_element(By.XPATH, '//div[contains(@class, "public-DraftStyleDefault-block")]/span').send_keys("Nice")
            send_btn = driver.find_element(By.XPATH, '//div[@aria-label="Send"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//a[@href="/messages"]').click()
            time.sleep(2)


def loop():
    while True:
        print('Its New2')
        reply_to_message()
        time.sleep(random.randrange(30, 60))
        retweet_new_tweet()
        time.sleep(random.randrange(30, 60))


if __name__ == '__main__':
    loop()
