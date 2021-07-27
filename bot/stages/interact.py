"""
Module for defining the bot twitter interaction flow.
"""
import proto.ad_pb2 as ad_pb2
import proto.bot_pb2 as bot_pb2
from selenium.webdriver import Chrome

from bot.stages.scraping_util import get_promoted_author
from bot.stages.scraping_util import get_timeline
from bot.stages.scraping_util import load_more_tweets
from bot.stages.scraping_util import refresh_page
from bot.stages.scraping_util import search_promoted_tweet_in_timeline
from bot.stages.scraping_util import take_element_screenshot

# This is just an aim - there is no guarantee this target will be met.
TARGET_AD_COUNT = 5


def interact(driver: Chrome, bot_username: str):
    """
    Executes the bot interaction flow and scrapes results.
    Ideas (TBD):
        - Have the driver auto-like the first 5 posts on their timeline - can this be done w/ the Twitter API instead?
    """
    _scrape(driver, bot_username)


def _scrape(driver: Chrome, bot_username: str):
    target = TARGET_AD_COUNT
    ad_collection = ad_pb2.AdCollection()
    while target > 0:
        timeline = get_timeline(driver)
        promoted_in_timeline = search_promoted_tweet_in_timeline(timeline)
        if promoted_in_timeline:
            # We must process this found tweet before refresh as the WebElement may no longer exist after
            bot = bot_pb2.Bot()
            bot.id = bot_username

            ad = ad_collection.ads.add()
            ad.bot.id = bot.id
            ad.content = promoted_in_timeline.text
            ad.promoter_handle = get_promoted_author(promoted_in_timeline)
            ad.screenshot = take_element_screenshot(promoted_in_timeline)

            refresh_page(driver)
        else:
            if not load_more_tweets(driver):
                refresh_page(driver)

        target -= 1