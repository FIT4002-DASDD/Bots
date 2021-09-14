"""
Entry point.
"""
import time
from datetime import datetime

from absl import app
from absl import flags
from absl import logging 
from datetime import datetime


from bot.stages.config import create_geckodriver
from bot.stages.interact import interact, agree_to_policy_updates_if_exists
from bot.stages.login import login_or_die

FLAGS = flags.FLAGS

flags.DEFINE_bool('debug', True, 'Whether to run in debug mode.')
flags.DEFINE_string('bot_username', None, 'Pass in bot username (required)')
flags.DEFINE_string('bot_password', None, 'Pass in bot password (required)')
flags.DEFINE_string('bot_output_directory', None,
                    'Pass in directory for storing bot output (required)')
flags.DEFINE_string('path_to_error_log', None, 'Pass in the path for error logging')

flags.register_validator('bot_username', lambda username: username and len(username) > 0,
                         message='Invalid username detected.')
flags.register_validator('bot_password', lambda pw: pw and len(pw) > 0, message='Invalid password detected.')

flags.mark_flags_as_required(['bot_username', 'bot_password', 'bot_output_directory'])


def main(argv):
    del argv  # Unused.
    _main()


# Wait before start of each stage.
STAGE_WAIT_DELAY = 5

# Wait before clicking on 'Ok' for policy updates after login
SHORT_WAIT = 3


def _main():
    logging.info(f'----------Started bot: {FLAGS.bot_username}----------')
    # Create the driver.
    driver = create_geckodriver()
    try:
        # Login.
        login_or_die(driver, FLAGS.bot_username, FLAGS.bot_password)

        # Agree to policy updates if presented.
        time.sleep(SHORT_WAIT)  # Wait to click on 'Ok' for policy updates
        agree_to_policy_updates_if_exists(driver)

        # Interact and Scrape.
        time.sleep(STAGE_WAIT_DELAY)
        interact(driver, FLAGS.bot_username)
    except Exception as e:  # Any exception raised will skip this cycle.
        logging.error(e)
        # Flush the current page source for debugging.
        if FLAGS.path_to_error_log:
            error_file = f'{FLAGS.path_to_error_log}/{FLAGS.bot_username}_' \
                         f'{datetime.now().strftime(r"%Y-%m-%d %H_%M_%S")}.html'
            with open(error_file, 'w') as f:
                f.write(driver.page_source)
            logging.info(f'Error file generated at: {error_file}')
    finally:
        logging.info('----------Cycle ended----------')
        # Cleanup.
        driver.quit()


if __name__ == '__main__':
    app.run(main)
