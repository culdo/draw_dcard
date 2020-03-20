import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import schedule


def login_and_draw(email, password):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://dcard.tw/signup')
    wait = WebDriverWait(browser, 10)
    try:
        id_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='email']")))
        id_input.click()
        id_input.send_keys(email)
        time.sleep(3)
        pwd_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']")))
        pwd_input.click()
        pwd_input.send_keys(password)
        time.sleep(3)
        submit_bt = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='註冊 / 登入']")))
        submit_bt.click()
        time.sleep(3)
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[title='抽卡']")))
        browser.get('https://dcard.tw/dcard')
        time.sleep(3)
        print(browser.execute_script("return document.documentElement.outerHTML"))
        invite_bt = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='送出邀請']")))
        invite_bt.click()
        greeting_msg = wait.until(
            EC.presence_of_element_located((By.NAME, "firstMessage")))
        greeting_msg.click()
        time.sleep(3)
        greeting_msg.send_keys("Hi")
        submit_msg = wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='送出']")))
        submit_msg.click()
        time.sleep(3)
    finally:
        browser.get('https://www.dcard.tw/signout')
        browser.quit()


if __name__ == '__main__':
    # login_and_draw(*sys.argv[1:])
    schedule.every().day.at("00:52").do(login_and_draw, *sys.argv[1:])

    while True:
        schedule.run_pending()
        time.sleep(1)
