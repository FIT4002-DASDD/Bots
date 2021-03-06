"""
Module for defining the bot twitter interaction flow.
"""
import time
from datetime import datetime
from random import random, randint
from typing import Union

import proto.ad_pb2 as ad_pb2
import proto.bot_pb2 as bot_pb2
from absl import flags
from absl import logging
from selenium.webdriver import Chrome, Firefox

from bot.stages.bot_info import get_bot
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
from bot.stages.scraping_util import get_tweet_content
from bot.stages.scraping_util import click_retry_loading

FLAGS = flags.FLAGS

# This is just an aim - there is no guarantee this target will be met.
TARGET_AD_COUNT = 4

# This is just an aim for how many tweets to retweet
TARGET_RETWEET_COUNT = 3

# Buffers ads until they need to be written out.
ad_collection = ad_pb2.AdCollection()


def interact(driver: Union[Firefox, Chrome], bot_username: str):
    """
    Executes the bot interaction flow and scrapes results.
    
    Parameters:
        driver: reference to the Webdriver instance
        bot_username: bot account's username
    """
    _scrape(driver, bot_username)
    # added randomisation to visiting account and retweeting/liking tweets
    if random() >= 0.5:
        retweet_posts(driver, bot_username)
    else:
        logging.info('Not visiting accounts this cycle, random probability generated was < 0.5')


def agree_to_policy_updates_if_exists(driver: Union[Firefox, Chrome]) -> None:
    """
    Click 'Ok' on the policy update pop-up if present.
    
    Parameters:
        driver: reference to the Webdriver instance
    """
    try:
        dialog = driver.find_element_by_xpath("//div[@role='dialog']")
        dialog.find_element_by_xpath(".//div[@role='button']").click()
        logging.info("Policy update pop-up found and clicked.")
    except:
        # No policy update found, continue as normal.
        return None


def _scrape(driver: Union[Firefox, Chrome], bot_username: str):
    """
    Scrapes the bot's timeline for Promoted content.
    
    Parameters:
        driver: reference to the Webdriver instance
    """
    bot = bot_pb2.Bot()
    bot.id = bot_username
    ad_collection.bot.id = bot.id

    target = TARGET_AD_COUNT
    while target > 0:
        timeline = get_timeline(driver)
        click_retry_loading(driver)
        promoted_in_timeline = search_promoted_tweet_in_timeline(timeline)
        sidebar = get_follow_sidebar(driver)
        promoted_in_follow_sidebar = search_promoted_follow_in_sidebar(sidebar)
        contents_and_likes = get_tweet_content(driver)
        refresh = False

        # Process tweets to find for tweets that have certain keywords for liking
        for element in range(0, len(contents_and_likes), 4):
            try:
                if any(tag in contents_and_likes[element].text for tag in get_bot(bot_username, 'relevant_tags')):
                    xpath_with_text = f'//span[contains(text(),"{contents_and_likes[element].text}")]//ancestor' \
                                      f'::div[4]//div[@data-testid="like"]'
                    like_button = driver.find_element_by_xpath(xpath_with_text)
                    like_button.click()
                    logging.info(bot_username + " liked a tweet.")
            except Exception as e:
                continue

        # NOTE: We must process found promoted content before refresh as the WebElement may no longer exist after.
        # Process Promoted Follow. We treat promoted follows similar to promoted tweets.
        if promoted_in_follow_sidebar:
            ad = ad_collection.ads.add()
            ad.ad_type = ad_pb2.Ad.AdType.AD_TYPE_FOLLOW
            ad.promoter_handle = get_promoted_follow(promoted_in_follow_sidebar)
            ad.created_at.GetCurrentTime()
            ad.seen_on = get_promoted_follow_link(promoted_in_follow_sidebar)

            refresh = True

        # Process Promoted Tweet.
        if promoted_in_timeline:
            ad = ad_collection.ads.add()
            ad.ad_type = ad_pb2.Ad.AdType.AD_TYPE_TWEET
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
    _write_out_ad_collection()


def _write_out_ad_collection():
    """
    Serializes the AdCollection proto and writes it out to a binary file.
    """
    # Path to the binary file containing the serialized protos for this bot.
    current_time = datetime.now()
    location = f'{FLAGS.bot_output_directory}/{FLAGS.bot_username}_{current_time.strftime("%Y%m%d")}_{int(current_time.timestamp())}_out'
    with open(location, 'wb') as f:
        f.write(ad_collection.SerializeToString())
        logging.info(f'Ad data for {FLAGS.bot_username} has been written out to: {location}')

        # Clear the ads.
        ad_collection.Clear()


def retweet_posts(driver: Union[Firefox, Chrome], bot_username: str) -> None:
    """
    Function to retweet/like posts from followed accounts.
    
    Parameters:
        driver: reference to the Webdriver instance
        bot_username: bot account's username
    """
    accounts = get_bot(bot_username, 'followed_accounts')
    accounts_to_visit = set()
    for i in range(0, randint(0, len(accounts))):
        accounts_to_visit.add(accounts[randint(0, len(accounts) - 1)])

    for account in accounts_to_visit:
        if visit_account(driver, account):
            # Call function to like tweets randomly
            like_post(driver, bot_username)
            buttons_to_retweet = driver.find_elements_by_xpath('//div[@data-testid="retweet"]')
            iterate = TARGET_RETWEET_COUNT if len(buttons_to_retweet) > TARGET_RETWEET_COUNT else len(
                buttons_to_retweet)
            for i in range(iterate):
                try:
                    if random() >= 0.5:
                        buttons_to_retweet[i].click()
                        logging.info("Clicked on retweet.")
                        # if a popup says 'are you sure you want to retweet before reading', this will retweet anyway
                        try:
                            driver.find_element_by_xpath('//div[@data-testid="retweetConfirm"]').click()
                            logging.info("Clicked on confirm retweet.")
                        except Exception as e:
                            continue
                except:
                    pass

                time.sleep(2)
            time.sleep(5)
        else:
            logging.error("Account visit failed.")


def like_post(driver: Union[Firefox, Chrome], bot_username: str) -> None:
    """
    Function to randomly like tweets.
    
    Parameters:
        driver: reference to the Webdriver instance
        bot_username: bot account's username
    """
    try:
        like_buttons = driver.find_elements_by_xpath('//div[@data-testid="like"]')
        for button in range(0, len(like_buttons)):
            # randomise tweets to like
            if random() >= 0.5:
                try:
                    like_buttons[button].click()
                    logging.info(bot_username + " liked a tweet.")
                except:
                    continue
    except Exception as e:
        pass

    return None


def visit_account(driver: Union[Firefox, Chrome], followed_account: str) -> bool:
    """
    Function to visit a Twitter account page.

    Parameters:
        driver: reference to the Webdriver instance
        followed_account: string of twitter account handle

    Returns:
        boolean that represents a successful/failed attempt at visiting the account
    """
    try:
        profile_url = 'https://twitter.com/' + followed_account
        driver.get(profile_url)
        time.sleep(3)
        if wait_for_page_load(driver):
            logging.info('Successfully visited account : ' + followed_account)
            return True
        return False

    except Exception as e:
        print(e)
        return False
