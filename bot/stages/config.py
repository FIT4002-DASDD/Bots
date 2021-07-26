"""
Module for app configuration.
"""
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('path_to_chromedriver', 'webdrivers/chromedriver', 'Pass in the path to chromedriver.')

WEBDRIVER_OPTIONS = [
    '--disable-blink-features=AutomationControlled',
    # '--headless',
    '--no-sandbox',
    '--disable-gpu'
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
]


def create_chromedriver() -> Chrome:
    op = Options()
    for arg in WEBDRIVER_OPTIONS:
        op.add_argument(arg)
    return Chrome(executable_path=FLAGS.path_to_chromedriver, options=op)
