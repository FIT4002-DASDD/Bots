"""
Module for defining the bot twitter interaction flow.
"""

from datetime import date, timedelta

import proto.ad_pb2 as ad_pb2
import proto.bot_pb2 as bot_pb2
from absl import flags
from absl import logging
from selenium.webdriver import Chrome

from bot.stages.scraping_util import get_promoted_author
from bot.stages.scraping_util import get_timeline
from bot.stages.scraping_util import load_more_tweets
from bot.stages.scraping_util import refresh_page
from bot.stages.scraping_util import search_promoted_tweet_in_timeline
from bot.stages.scraping_util import take_element_screenshot

FLAGS = flags.FLAGS

# This is just an aim - there is no guarantee this target will be met.
TARGET_AD_COUNT = 5

# Buffers ads until they need to be written out.
ad_collection = ad_pb2.AdCollection()

# Tracks when the AdCollection was last written out.
LAST_WRITTEN_OUT = date.today() - timedelta(days=1)  # Subtract one day so we write out on the first invocation.


def interact(driver: Chrome, bot_username: str):
    """
    Executes the bot interaction flow and scrapes results.
    Ideas (TBD):
        - Have the driver auto-like the first 5 posts on their timeline - can this be done w/ the Twitter API instead?
    """
    _scrape(driver, bot_username)

# Function to click 'Ok' on the policy update pop-up
def agree_to_policy_updates(driver: Chrome):
    try:
        dialog = driver.find_element_by_xpath("//div[@role='dialog']")
        dialog.find_element_by_xpath(".//div[@role='button']").click()
    except Exception as e:
        logging.info("[UNSURE] No policy update pop-up.")

def _scrape(driver: Chrome, bot_username: str):
    """Scrapes the bot's timeline for Promoted tweets"""
    target = TARGET_AD_COUNT
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
            ad.created_at.GetCurrentTime()  # This sets the field:  https://stackoverflow.com/a/65138505/15507541

            refresh_page(driver)
        else:
            if not load_more_tweets(driver):
                refresh_page(driver)

        target -= 1

    if _should_flush_ad_collection():
        logging.info('Writing out AdCollection as one day has elapsed.')
        _write_out_ad_collection()


def _should_flush_ad_collection() -> bool:
    """
    Whether the ads stored in the AdCollection need to be written out.
    Ads will be flushed ONCE a DAY.
    """
    date_today = date.today()
    return date_today > LAST_WRITTEN_OUT


def _write_out_ad_collection():
    """Serializes the AdCollection proto and writes it out to a binary file."""
    global LAST_WRITTEN_OUT
    # Update when the collection was last written out.
    LAST_WRITTEN_OUT = date.today()

    # Path to the binary file containing the serialized protos for this bot.
    location = f'{FLAGS.bot_output_directory}/{FLAGS.bot_username}_{LAST_WRITTEN_OUT.strftime("%Y-%m-%d")}_out'
    with open(location, 'wb') as f:
        f.write(ad_collection.SerializeToString())
        logging.info(f'Ad data for {FLAGS.bot_username} has been written out to: {location}')

    # Clear the ads.
    ad_collection.Clear()

def like_post(driver: Chrome):
    # driver.find_element_by_xpath('//div[aria-label*="Likes. Like"]')