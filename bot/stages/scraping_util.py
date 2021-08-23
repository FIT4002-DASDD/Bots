"""
Contains utilities to help with scraping.
Ref: https://github.com/kautzz/twitter-problock
"""
import time
from typing import Union

from absl import flags
from absl import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FLAGS = flags.FLAGS

SCREENSHOT_COUNT = 1


def get_timeline(driver: Union[Firefox, Chrome]) -> WebElement:
    """Returns a twitter timeline WebElement."""
    return driver.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")


def take_element_screenshot(web_element: WebElement) -> str:
    """
    Screenshots a given WebElement, returning it as a base-64 string.
    If running in Debug mode, the PNG file is also saved to the bot's output directory.
    """
    if FLAGS.debug:
        _take_screenshot_and_save_to_file(web_element)
    return web_element.screenshot_as_base64


def _take_screenshot_and_save_to_file(web_element: WebElement):
    global SCREENSHOT_COUNT
    screenshot_filename = f'{FLAGS.bot_output_directory}/{FLAGS.bot_username}_{SCREENSHOT_COUNT}.png'
    if web_element.screenshot(screenshot_filename):
        logging.info(f'Successfully captured screenshot: {screenshot_filename}')
        SCREENSHOT_COUNT += 1


def wait_for_page_load(driver: Union[Firefox, Chrome]) -> bool:
    logging.info('Waiting for page load...')

    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='progressbar']/following::div[contains(@style, '26px')]")))
    except Exception as e:
        print(e)
        logging.error('Could not trigger loading of new content.')

    try:
        WebDriverWait(driver, 7).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@role='progressbar']/following::div[contains(@style, '26px')]")))
    except Exception as e:
        print(e)
        logging.error('Timed out waiting for new content.')
        return False

    logging.info('New content loaded...')
    return True


def load_more_tweets(driver: Union[Firefox, Chrome]) -> bool:
    logging.info('Scrolling to lazy load more tweets...')

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    return wait_for_page_load(driver)


def refresh_page(driver: Union[Firefox, Chrome]) -> bool:
    logging.info('Refreshing page...')

    driver.refresh()
    return wait_for_page_load(driver)


def search_promoted_tweet_in_timeline(timeline: WebElement) -> Union[WebElement, None]:
    logging.info('Searching timeline for promoted tweets...')

    try:
        promoted = timeline.find_element(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[4]")
        logging.info('Found a promoted tweet.')
        return promoted
    except NoSuchElementException:
        logging.info('No promoted tweet found.')
        return None


def get_promoted_author(promoted_tweet: WebElement) -> str:
    promoter = promoted_tweet.find_element(By.XPATH, ".//*[contains(text(), '@')]")
    return promoter.get_attribute('innerHTML')


def get_promoted_tweet_link(promoted_tweet: WebElement, driver: Chrome) -> str:
    """
    This function can scrape tweet link for the promoted tweet, this is the link inside the tweeter

    Parameters:
        promoted_tweet: WebElement for the promoted tweet
        driver: web driver

    Returns:
        tweet_link: tweet link for the promoted tweet, this is the link inside the tweeter
    """
    previous_url = driver.current_url
    try:
        promoted_icon = promoted_tweet.find_element(By.XPATH, ".//*[contains(text(), 'Promoted')]")
        promoted_icon.click()
        max_wait_time = 10
        current_wait_time = 0
        while previous_url == driver.current_url or current_wait_time < max_wait_time:
            current_wait_time += 1
            time.sleep(0.5)
        tweet_link = driver.current_url
        if previous_url != tweet_link:
            driver.back()
            logging.info("Tweet link scraped successfully: " + tweet_link)
        else:
            tweet_link = ""
            logging.info("Tweet link scrape failed")
    except Exception as e:
        print(e)
        if previous_url != driver.current_url:
            driver.back()
        tweet_link = ""
        logging.info("Tweet link scrape failed")
    return tweet_link


def get_promoted_tweet_official_link(promoted_tweet: WebElement) -> str:
    """
    This function can scrape official link for the promoted tweet, this is the link which take you outside the tweeter and navigate you to the official website of the Ads

    Parameters:
        promoted_tweet: WebElement for the promoted tweet

    Returns:
        tweet_official_link: official link for the promoted tweet, this is the link which take you outside the tweeter and navigate you to the official website of the Ads
    """
    try:
        list_of_element = promoted_tweet.find_elements(By.XPATH,
                                                       ".//*[contains(text(), 'Promoted')]//ancestor::div[4]//a[@role = 'link']")
        tweet_official_link = list_of_element[-1].get_attribute('href')
        logging.info("Official link scraped successfully: " + tweet_official_link)
    except Exception as e:
        print(e)
        tweet_official_link = ""
        logging.info("Official link scrape failed")
    return tweet_official_link
