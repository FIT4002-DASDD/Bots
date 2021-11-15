"""
Module for app configuration.
"""
from absl import flags
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as GeckoOptions

FLAGS = flags.FLAGS

flags.DEFINE_string('path_to_chromedriver',
                    'webdrivers/chromedriver', 'Pass in the path to chromedriver.')
flags.DEFINE_string('path_to_geckodriver',
                    'webdrivers/geckodriver', 'Pass in the path to geckodriver.')

# List containing all the options for the webdriver. E.g. headless webdriver
WEBDRIVER_OPTIONS = [
    '--disable-blink-features=AutomationControlled',
    '--headless',
    '--no-sandbox',
    '--disable-gpu',
    '--window-size=1280x720',
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
]


def create_chromedriver() -> Chrome:
    """Function to instantiate a Chrome webdriver."""
    op = ChromeOptions()
    for arg in WEBDRIVER_OPTIONS:
        op.add_argument(arg)
    return Chrome(executable_path=FLAGS.path_to_chromedriver, options=op)


def create_geckodriver() -> Firefox:
    """Function to instantiate a Firefox webdriver."""
    op = GeckoOptions()
    for arg in WEBDRIVER_OPTIONS:
        op.add_argument(arg)
    return Firefox(executable_path=FLAGS.path_to_geckodriver, options=op)
