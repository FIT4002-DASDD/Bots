"""
Module for app configuration.
"""
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('path_to_chromedriver', 'webdrivers/chromedriver', 'Pass in the path to chromedriver.')

WEBDRIVER_OPTIONS = [
    '--disable-blink-features=AutomationControlled',
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--window-size=1280x720',
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
]

def create_geckodriver() -> Firefox:
    op = Options()
    for arg in WEBDRIVER_OPTIONS:
        op.add_argument(arg)
    driver = Firefox(executable_path="webdrivers/geckodriver", options=op)
    return driver
