"""
Module for logging into a Twitter account.
"""
import time
from typing import Union

from absl import logging, flags
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bot.stages.scraping_util import wait_for_page_load
from bot.stages.interact import get_bot

FLAGS = flags.FLAGS

TWITTER_LOGIN_URL = 'https://twitter.com/login'

LOGIN_WAIT = 10
VERIFICATION_WAIT = 3

def login_or_die(driver: Union[Firefox, Chrome], username: str, password: str):
    if not _login(driver, username, password):
        raise Exception('FAILURE. Log in was not successful.')


def _login(driver: Union[Firefox, Chrome], username: str, password: str) -> bool:
    try:
        driver.get(TWITTER_LOGIN_URL)

        e_username = WebDriverWait(driver, LOGIN_WAIT).until(
            EC.visibility_of_element_located((By.NAME, 'session[username_or_email]')))
        e_pw = driver.find_element_by_name('session[password]')

        e_username.send_keys(username)
        e_pw.send_keys(password)
        e_pw.send_keys(Keys.RETURN)
    except Exception as e:
        logging.info("UNSURE: Alternate login screen shown.")
        try:
            alternate_screen_login(driver, username, password)
        except Exception as e:
            logging.info(e)
            return False        

    time.sleep(VERIFICATION_WAIT)
    verify_phone_number(driver, username)

    if wait_for_page_load(driver):
        logging.info('Successfully logged in.')
        return True
    else:
        return False

def alternate_screen_login(driver: Union[Firefox, Chrome], bot_username: str, bot_password: str) -> None:
    """Function to login with the alternate Twitter login interface."""
    try:
        username = driver.find_element_by_name("username")
        username.send_keys(bot_username)
        username.send_keys(Keys.RETURN)

        time.sleep(2)
        password = driver.find_element(By.NAME, "password")
        password.send_keys(bot_password)
        password.send_keys(Keys.RETURN)
    except:
        return None

def verify_phone_number(driver: Union[Firefox, Chrome], bot_username: str) -> None:
    """Key-in phone number if phone number verification is presented."""
    try:
        ACCOUNT_PHONE_NUMBER = get_bot(bot_username, 'NUMBER')
        xpath = "//strong[contains(text(), 'Your phone number ends in " + ACCOUNT_PHONE_NUMBER[-2:] + "')]"
        # To ensure that the verification required is phone number verification.
        hint = driver.find_element_by_xpath(xpath)
        # hint = driver.find_element_by_xpath("//strong[contains(text(), 'Your phone number ends in 38')]")

        # Find the element to fill the phone number detail.
        phone_number = driver.find_element_by_name('challenge_response')

        # Fill in the element with phone number.
        phone_number.send_keys(ACCOUNT_PHONE_NUMBER)

        # Hit enter.
        phone_number.send_keys(Keys.RETURN)
        logging.info('Keyed in phone number for verification.')
    except:
        # We didn't need to verify phone number, continue as normal.
        return None
