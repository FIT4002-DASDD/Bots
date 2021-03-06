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
    """
    Function that returns a twitter timeline WebElement.

    Parameters:
        driver: reference to the Webdriver instance

    Returns:
        web element of the twitter timeline
    """
    try:
        return driver.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")
    except:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@data-testid='primaryColumn']")))
        return driver.find_element(By.XPATH, "//div[@data-testid='primaryColumn']")


def get_follow_sidebar(driver: Union[Firefox, Chrome]) -> WebElement:
    """
    Function that returns a twitter "Who to follow" sidebar WebElement.

    Parameters:
        driver: reference to the Webdriver instance

    Returns:
        web element of the twitter "Who to follow" sidebar
    """
    try:
        return driver.find_element(By.XPATH, "//aside[@aria-label='Who to follow']")
    except:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, "//aside[@aria-label='Who to follow']")))
        return driver.find_element(By.XPATH, "//aside[@aria-label='Who to follow']")


def take_element_screenshot(web_element: WebElement) -> str:
    """
    Screenshots a given WebElement, returning it as a PNG bytestring.
    If running in Debug mode, the PNG file is also saved to the bot's output directory.
        
    Parameters:
        web_element: reference to the web element to screenshot

    Returns:
        a PNG bytestring containing the image
    """
    if FLAGS.debug:
        _take_screenshot_and_save_to_file(web_element)
    return web_element.screenshot_as_png


def _take_screenshot_and_save_to_file(web_element: WebElement):
    """
    Function to take screenshot and save to a file.

    Parameters:
        web_element: reference to the web element to screenshot
    """
    global SCREENSHOT_COUNT
    screenshot_filename = f'{FLAGS.bot_output_directory}/{FLAGS.bot_username}_{SCREENSHOT_COUNT}.png'
    if web_element.screenshot(screenshot_filename):
        logging.info(f'Successfully captured screenshot: {screenshot_filename}')
        SCREENSHOT_COUNT += 1


def wait_for_page_load(driver: Union[Firefox, Chrome]) -> bool:
    """
    Function to wait for page to load.
    
    Parameters:
        driver: reference to the Webdriver instance

    Returns:
        boolean that represents a successful/failed page load
    """
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
    """
    Function to load more tweets. It simulates scrolling the page downwards to lazy load more tweets.
    
    Parameters:
        driver: reference to the Webdriver instance

    Returns:
        boolean that represents a successful/failed page load
    """
    logging.info('Scrolling to lazy load more tweets...')

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    return wait_for_page_load(driver)


def refresh_page(driver: Union[Firefox, Chrome]) -> bool:
    """
    Function to refresh the current page.
    
    Parameters:
        driver: reference to the Webdriver instance

    Returns:
        boolean that represents a successful/failed page refresh
    """
    logging.info('Refreshing page...')

    driver.refresh()
    return wait_for_page_load(driver)


def search_promoted_tweet_in_timeline(timeline: WebElement) -> Union[WebElement, None]:
    """
    Function to search for promoted tweet in Twitter timeline.

    Parameters:
        timeline: reference the timeline web element

    Returns:
        web element that represents the promoted tweet or none if not found
    """
    logging.info('Searching timeline for promoted tweets...')

    try:
        promoted = timeline.find_element(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[4]")
        logging.info('Found a promoted tweet.')
        return promoted
    except NoSuchElementException:
        logging.info('No promoted tweet found.')
        return None


def search_promoted_follow_in_sidebar(sidebar: WebElement) -> Union[WebElement, None]:
    """
    Function to search for promoted accounts to follow in the sidebar of the page.

    Parameters:
        sidebar: reference the sidebar web element

    Returns:
        web element that represents the promoted accounts to follow in the sidebar of the page.
    """
    logging.info('Searching sidebar for promoted follows...')

    try:
        promoted = sidebar.find_element(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[5]")
        logging.info('Found a promoted follow.')
        return promoted
    except NoSuchElementException:
        logging.info('No promoted follow found.')
        return None


def get_promoted_author(promoted_tweet: WebElement) -> str:
    """
    Function to get the promoted author of a promoted tweet.

    Parameters:
        promoted_tweet: the promoted tweet web element

    Returns:
        string of the promoted author
    """
    promoter = promoted_tweet.find_element(By.XPATH, ".//*[contains(text(), '@')]")
    return promoter.get_attribute('innerHTML')


def get_promoted_tweet_link(promoted_tweet: WebElement, driver: Chrome) -> str:
    """
    This function can scrape the link of a promoted tweet.

    Parameters:
        promoted_tweet: WebElement for the promoted tweet
        driver: reference to the webdriver

    Returns:
        tweet_link: tweet link of the promoted tweet.
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
    This function can scrape official link for the promoted tweet; this is the link which takes you outside Twitter
    to the official website of the promoted Ad.

    Parameters:
        promoted_tweet: WebElement for the promoted tweet

    Returns: tweet_official_link: the official link present in the promoted Ad.
    """
    try:
        list_of_element = promoted_tweet.find_elements(By.XPATH,
                                                       ".//*[contains(text(), 'Promoted')]//ancestor::div[4]//a[@role "
                                                       "= 'link']")
        tweet_official_link = list_of_element[-1].get_attribute('href')
        logging.info("Official link scraped successfully: " + tweet_official_link)
    except Exception as e:
        print(e)
        tweet_official_link = ""
        logging.info("Official link scrape failed")
    return tweet_official_link


def get_promoted_follow(promoted_follow: WebElement) -> str:
    """
    Returns the twitter handle of an account promoted as a follow suggestion.

    Parameters:
        promoted_follow: WebElement for the promoted follow suggestion

    Returns:
        the handle of the promoted account as a string
    """
    try:
        promoter = promoted_follow.find_element(By.XPATH, ".//*[contains(text(), '@')]")
        handle = promoter.get_attribute('innerHTML')
        logging.info("Scraped promoted follow: " + handle)
    except Exception as e:
        print(e)
        handle = ""
        logging.info("Promoted follow handle scrape failed")
    return handle


def get_promoted_follow_link(promoted_follow: WebElement) -> str:
    """
    Function that returns the link of an account promoted as a follow suggestion.

    Parameters:
        promoted_follow: WebElement for the promoted follow suggestion

    Returns:
        the link of the promoted follow as a string
    """
    try:
        link = promoted_follow.find_element(By.XPATH, ".//a").get_attribute('href')
    except Exception as e:
        print(e)
        link = ""
        logging.info("Follow link scrape failed")
    return link


def get_tweet_content(driver: Union[Firefox, Chrome]) -> WebElement:
    """
    Function that returns a web element that contains the tweet contents.

    Parameters:
        driver: reference to the Webdriver

    Returns:
        the web element of the tweet with contents
    """
    
    try:
        return driver.find_elements_by_xpath('//div[@data-testid="like"]//ancestor::div[4]/child::div[1]')
    except:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="like"]//ancestor::div[4]/child::div[1]')))
        return driver.find_elements_by_xpath('//div[@data-testid="like"]//ancestor::div[4]/child::div[1]')

def click_retry_loading(driver: Union[Firefox, Chrome]) -> None:
    """
    Function to click retry loading to ensure the timeline and sidebar loads elements.

    Parameters:
        driver: reference to the Webdriver
    """
    try:
        buttons = driver.find_elements_by_xpath('//span[contains(text(), "Retry")]')
        for button in buttons:
            button.click()

        if not wait_for_page_load(driver):
            refresh_page(driver)
        return None
    except:
        return None
