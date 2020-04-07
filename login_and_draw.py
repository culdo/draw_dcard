import sys
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email_notification import send_mail
from selenium.common.exceptions import TimeoutException
import schedule

curl_cmd = "curl --http2 -X GET -H 'Host:www.dcard.tw' " \
           "-H 'user-agent:Dcard-Android/7.22.2; Dalvik/2.1.0 (Linux; U; Android 9; Mi A1 MIUI/V10.0.14.0.PDHMIXM); DcardWebView;' " \
           "-H 'authorization:Bearer 0YIJMPy4SMiMhuQ0Vk8ZKw==' " \
           "-H 'content-type:application/x-www-form-urlencoded' " \
           "-H 'accept-encoding:gzip' " \
           "-H 'if-none-match:W/'330-VI1bKvdXqz4o7jZiYiV0oYVLO7s'' 'https://www.dcard.tw/v2/dcard'"


def login_and_draw(email, password):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://dcard.tw/signup')
    wait = WebDriverWait(browser, 10)
    try:
        id_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
        id_input.click()
        id_input.send_keys(email)
        time.sleep(random.randint(2, 5))
        pwd_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
        pwd_input.click()
        pwd_input.send_keys(password)
        time.sleep(random.randint(2, 5))
        submit_bt = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='註冊 / 登入']")))
        submit_bt.click()
        time.sleep(random.randint(2, 5))
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[title='抽卡']")))
        browser.get('https://dcard.tw/dcard')
        time.sleep(random.randint(2, 5))
        print(browser.execute_script("return document.documentElement.outerHTML"))
        invite_bt = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='送出邀請']")))
        invite_bt.click()
        greeting_msg = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[placeholder='用簡短的問候開啟話題吧！']")))
        greeting_msg.click()
        greeting_msg.clear()
        time.sleep(random.randint(2, 5))
        greeting_msg.send_keys("Hi~")
        submit_msg = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='完成']")))
        submit_msg.click()
        time.sleep(random.randint(2, 5))
    except Exception as e:
        send_mail("wuorsut@gmail.com", "Auto Draw Dcard", "error: %s" % str(e))
    finally:
        browser.get('https://www.dcard.tw/signout')
        browser.quit()


if __name__ == '__main__':
    login_and_draw(*sys.argv[1:])
    # Draw dcard at random hour of one day.
    schedule.every(25).to(47).hours.do(login_and_draw, *sys.argv[1:])
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
