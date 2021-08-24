"""
Entry point.
"""
from schedule import every, repeat, run_pending
import time

from absl import app
from absl import flags
from absl import logging

from bot.stages.config import create_chromedriver
from bot.stages.login import login_or_die
from bot.stages.interact import interact, agree_to_policy_updates

FLAGS = flags.FLAGS

flags.DEFINE_bool('debug', True, 'Whether to run in debug mode.')
flags.DEFINE_string('bot_username', None, 'Pass in bot username (required)')
flags.DEFINE_string('bot_password', None, 'Pass in bot password (required)')
flags.DEFINE_string('bot_output_directory', None, 'Pass in directory for storing bot output (required)')

flags.register_validator('bot_username', lambda username: username and len(username) > 0,
                         message='Invalid username detected.')
flags.register_validator('bot_password', lambda pw: pw and len(pw) > 0, message='Invalid password detected.')

flags.mark_flags_as_required(['bot_username', 'bot_password', 'bot_output_directory'])


def main(argv):
    del argv  # Unused.
    _main()
    while True:
        run_pending()
        time.sleep(1)


# Wait before start of each stage.
STAGE_WAIT_DELAY = 5
SHORT_WAIT = 3

# Bot flow should run periodically.
@repeat(every().hour)
def _main():
    logging.info(f'----------Started bot: {FLAGS.bot_username}----------')

    try:
        # Create the driver.
        driver = create_chromedriver()

        # Login.
        login_or_die(driver, FLAGS.bot_username, FLAGS.bot_password)

        # Wait to click on 'Ok' for policy updates
        time.sleep(SHORT_WAIT)
        agree_to_policy_updates(driver)

        # Interact and Scrape.
        time.sleep(STAGE_WAIT_DELAY)
        interact(driver, FLAGS.bot_username)
        
        # Cleanup.
        driver.quit()

    except Exception as e:  # Any exception raised will skip this cycle.
        logging.error(e)
    finally:
        logging.info('----------Cycle ended----------')


if __name__ == '__main__':
    app.run(main)
