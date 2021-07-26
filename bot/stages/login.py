"""
Module for logging into a Twitter account.
"""
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from absl import logging

TWITTER_LOGIN_URL = 'https://twitter.com/login'
LOGIN_WAIT = 10


def login_or_die(driver: Chrome, username: str, password: str):
    if not _login(driver, username, password):
        driver.quit()
        logging.fatal('FAILURE. Log in was not successful.')


def _login(driver: Chrome, username: str, password: str) -> bool:
    try:
        driver.get(TWITTER_LOGIN_URL)

        e_username = WebDriverWait(driver, LOGIN_WAIT).until(
            EC.visibility_of_element_located((By.NAME, 'session[username_or_email]')))
        e_pw = driver.find_element_by_name('session[password]')

        e_username.send_keys(username)
        e_pw.send_keys(password)
        e_pw.send_keys(Keys.RETURN)

        logging.info('Successfully logged in.')
        return True  # TODO: detect successful login properly
    except Exception as e:
        print(e)
        return False
