"""
Contains utilities to help with scraping.
"""
from selenium.webdriver.remote.webelement import WebElement
from absl import flags

FLAGS = flags.FLAGS

SCREENSHOT_COUNT = 1


def take_element_screenshot(web_element: WebElement) -> str:
    if FLAGS.debug:
        web_element.screenshot(f'bot_out/{FLAGS.bot_username}_{SCREENSHOT_COUNT}.png')

    return web_element.screenshot_as_base64()
