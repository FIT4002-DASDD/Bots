"""
Module for defining the bot twitter interaction flow.
"""
from selenium.webdriver import Chrome

from bot.stages.scraping_util import get_timeline
from bot.stages.scraping_util import take_element_screenshot


def interact(driver: Chrome):
    timeline = get_timeline(driver)
    take_element_screenshot(timeline)

    # just like the first 5 posts? - maybe do this with the Twitter API!
