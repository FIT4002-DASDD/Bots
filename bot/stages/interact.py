"""
Module for defining the bot twitter interaction flow.
"""
import time
from datetime import date, timedelta
from typing import Union

import proto.ad_pb2 as ad_pb2
import proto.bot_pb2 as bot_pb2
from absl import flags
from absl import logging
from selenium.common import exceptions
from selenium.webdriver import Chrome, Firefox

from bot.stages.bot_info import bots
from bot.stages.scraping_util import get_follow_sidebar
from bot.stages.scraping_util import get_promoted_author
from bot.stages.scraping_util import get_promoted_follow
from bot.stages.scraping_util import get_promoted_follow_link
from bot.stages.scraping_util import get_promoted_tweet_link
from bot.stages.scraping_util import get_promoted_tweet_official_link
from bot.stages.scraping_util import get_timeline
from bot.stages.scraping_util import load_more_tweets
from bot.stages.scraping_util import refresh_page
from bot.stages.scraping_util import search_promoted_follow_in_sidebar
from bot.stages.scraping_util import search_promoted_tweet_in_timeline
from bot.stages.scraping_util import take_element_screenshot
from bot.stages.scraping_util import wait_for_page_load

FLAGS = flags.FLAGS

# This is just an aim - there is no guarantee this target will be met.
TARGET_AD_COUNT = 2

# This is just an aim for how many tweets to retweet
TARGET_RETWEET_COUNT = 3
# This is just an aim for how many times to load more tweets by scrolling down the page
TARGET_SCROLL_COUNT = 10

# Buffers ads until they need to be written out.
ad_collection = ad_pb2.AdCollection()

# Tracks when the AdCollection was last written out.
# Subtract one day so we write out on the first invocation.
LAST_WRITTEN_OUT = date.today() - timedelta(days=1)


def interact(driver: Union[Firefox, Chrome], bot_username: str):
    """
    Executes the bot interaction flow and scrapes results.
    Ideas (TBD):
        - Have the driver auto-like the first 5 posts on their timeline - can this be done w/ the Twitter API instead?
    """
    _scrape(driver, bot_username)


def agree_to_policy_updates_if_exists(driver: Union[Firefox, Chrome]) -> None:
    """Click 'Ok' on the policy update pop-up if present."""
    try:
        dialog = driver.find_element_by_xpath("//div[@role='dialog']")
        dialog.find_element_by_xpath(".//div[@role='button']").click()
        logging.info("Policy update pop-up found and clicked.")
    except Exception as e:
        # No policy update found, continue as normal.
        return None


def _scrape(driver: Union[Firefox, Chrome], bot_username: str):
    """Scrapes the bot's timeline for Promoted content."""
    bot = bot_pb2.Bot()
    bot.id = bot_username
    ad_collection.bot.id = bot.id

    target = TARGET_AD_COUNT
    while target > 0:
        timeline = get_timeline(driver)
        promoted_in_timeline = search_promoted_tweet_in_timeline(timeline)
        sidebar = get_follow_sidebar(driver)
        promoted_in_follow_sidebar = search_promoted_follow_in_sidebar(sidebar)
        refresh = False

        # NOTE: We must process found promoted content before refresh as the WebElement may no longer exist after.
        # Process Promoted Follow. We treat promoted follows the same as promoted ads.
        if promoted_in_follow_sidebar:
            ad = ad_collection.ads.add()
            ad.promoter_handle = get_promoted_follow(promoted_in_follow_sidebar)
            ad.created_at.GetCurrentTime()
            ad.seen_on = get_promoted_follow_link(promoted_in_follow_sidebar)

            refresh = True

        # Process Promoted Tweet.
        if promoted_in_timeline:
            ad = ad_collection.ads.add()
            ad.content = promoted_in_timeline.text
            ad.promoter_handle = get_promoted_author(promoted_in_timeline)
            ad.screenshot = take_element_screenshot(promoted_in_timeline)
            ad.created_at.GetCurrentTime()  # This sets the field:  https://stackoverflow.com/a/65138505/15507541
            ad.official_ad_link = get_promoted_tweet_official_link(promoted_in_timeline)
            ad.seen_on = get_promoted_tweet_link(promoted_in_timeline, driver)

            refresh = True

        if refresh:
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
    return date.today() > LAST_WRITTEN_OUT


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


def like_post(driver: Chrome, bot_username: str) -> None:
    """TBD."""
    bot = None
    try:
        count = 0
        found = False
        while not found:
            if bot_username != bots[0]['username']:
                count += 1
            bot = bots[count]
            found = True
    except:
        logging.error("Bot does not exist in bot_info.py")

    tags_to_include = bot['relevant_tags']
    count = 0
    while count < TARGET_SCROLL_COUNT:
        try:
            contents_and_likes = driver.find_elements_by_xpath(
                '//div[@data-testid="like"]//ancestor::div[4]/child::div[1]')
            for element in range(0, len(contents_and_likes), 4):
                try:
                    if any(tag in contents_and_likes[element].text for tag in tags_to_include):
                        xpath_with_text = f'//span[contains(text(),"{contents_and_likes[element].text}")]//ancestor' \
                                          f'::div[4]//div[@data-testid="like"] '
                        like_button = driver.find_element_by_xpath(xpath_with_text)
                        like_button.click()
                except exceptions.StaleElementReferenceException as e:
                    continue

            load_more_tweets(driver)
            count += 1

        except Exception as e:
            count += 1
            continue

    return None


def retweet_posts(driver: Chrome, bot_username: str) -> None:
    """TBD."""
    bot = None
    try:
        count = 0
        found = False
        while not found:
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
                continue

            time.sleep(2)
        time.sleep(5)

    return None


def visit_account(driver: Chrome, followed_account: str) -> bool:
    """TBD."""
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
