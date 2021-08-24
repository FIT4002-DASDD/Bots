"""
Module for defining the bot twitter interaction flow.
"""

from datetime import date, timedelta

import proto.ad_pb2 as ad_pb2
import proto.bot_pb2 as bot_pb2
from absl import flags
from absl import logging
from selenium.webdriver import Chrome
from selenium.common import exceptions

from bot.stages.scraping_util import get_promoted_author, wait_for_page_load
from bot.stages.scraping_util import get_timeline
from bot.stages.scraping_util import load_more_tweets
from bot.stages.scraping_util import refresh_page
from bot.stages.scraping_util import search_promoted_tweet_in_timeline
from bot.stages.scraping_util import take_element_screenshot
from bot.stages.bot_info import bots
import time

FLAGS = flags.FLAGS

# This is just an aim - there is no guarantee this target will be met.
TARGET_AD_COUNT = 5

TARGET_RETWEET_COUNT = 3

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
    # _scrape(driver, bot_username)
    # like_post(driver, bot_username)
    retweet_posts(driver, bot_username)


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

# WORK IN PROGRESS
def like_post(driver: Chrome, bot_username: str):
    bot = None
    try:
        count = 0
        found = False
        while found == False:
            if bot_username != bots[0]['username']:
                count += 1
            bot = bots[count]
            found = True
    except:
        logging.error("Bot does not exist in bot_info.py")

    tags_to_include = bot['relevant_tags']
    try:
        # current_posts = driver.execute_script(r'''return document.querySelectorAll('[aria-label*="Likes. Like"]')''')
        # current_posts = driver.execute_script(r'''return document.querySelectorAll('[data-testid="like"]')''')
        contents_and_likes = driver.find_elements_by_xpath('//div[@data-testid="like"]//ancestor::div[4]/child::div[1]')
        print(len(contents_and_likes))
        for element in range(0, len(contents_and_likes), 4):
            try:
                if contents_and_likes[element].text in tags_to_include:
                    contents_and_likes[element-1].click()
            except exceptions.StaleElementReferenceException as e:
                pass
        
    except Exception as e:
        pass
        

# WORK IN PROGRESS
def retweet_posts(driver: Chrome, bot_username: str):
    bot = None
    try:
        count = 0
        found = False
        while found == False:
            if bot_username != bots[0]['username']:
                count += 1
            bot = bots[count]
            found = True
    except:
        logging.error("Bot does not exist in bot_info.py")

    followed_accounts = bot['followed_accounts']

    for account in followed_accounts:
        visit_account(driver, account)
        buttons_to_retweet = driver.find_elements_by_xpath('//div[@data-testid="retweet"]')
        iterate = TARGET_RETWEET_COUNT if len(buttons_to_retweet) > TARGET_RETWEET_COUNT else len(buttons_to_retweet)
        for i in range(iterate):
            buttons_to_retweet[i].click()

            # in case a popup says 'are you sure you want to retweet before reading', this will retweet anyway
            try:
                driver.find_element_by_xpath('//div[@data-testid="retweetConfirm"]').click()
            except Exception as e:
                pass
            time.sleep(2)
        time.sleep(5)

def visit_account(driver: Chrome, followed_account: str):
    try:
        profile_url = 'https://twitter.com/' + followed_account
        driver.get(profile_url)

        if wait_for_page_load(driver):
            logging.info('Successfully visited account : ' + followed_account)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False