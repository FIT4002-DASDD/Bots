"""
Contains utilities to help with scraping.
"""
from absl import flags
from absl import logging
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

FLAGS = flags.FLAGS

SCREENSHOT_COUNT = 1


def take_element_screenshot(web_element: WebElement) -> str:
    if FLAGS.debug:
        web_element.screenshot(f'bot_out/{FLAGS.bot_username}_{SCREENSHOT_COUNT}.png')

    return web_element.screenshot_as_base64()


# Credit: https://github.com/kautzz/twitter-problock
def wait_for_page_load(driver: Chrome) -> bool:
    logging.info('Waiting for page load...')

    try:
        WebDriverWait(driver, 2).until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='progressbar']/following::div[contains(@style, '26px')]")))
    except Exception as e:
        print(e)
        logging.error('Could not trigger loading of new content.')
        return False

    try:
        WebDriverWait(driver, 7).until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[@role='progressbar']/following::div[contains(@style, '26px')]")))
    except Exception as e:
        print(e)
        logging.error('Timed out waiting for new content.')
        return False

    logging.info('New content loaded...')
    return True
