"""
Testing scraping util functionality.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock, Mock

from absl import flags
from selenium.webdriver.common.by import By

from bot.stages.scraping_util import get_timeline, take_element_screenshot


class ScrapingUtilTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Configures the flags needed by the module.
        """
        flags.DEFINE_boolean('debug', False, '')
        flags.DEFINE_string('bot_output_directory', '', '')
        flags.DEFINE_string('bot_username', '', '')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tears down code artifacts used for testing across all tests.
        @note: runs only once for each test class as opposed to tearDown()
        :return:
        """
        pass

    def setUp(self) -> None:
        """
        Sets up code artifacts to be used for testing prior to running each individual test case.
        """
        self.mock_driver = MagicMock()
        self.flags = flags.FLAGS
        # Forcefully mark the flags as parsed.
        self.flags.mark_as_parsed()

    def tearDown(self) -> None:
        """
        Tears down code artifacts used for testing created in the setUp().
        :return:
        """
        self.mock_driver = None
        self.flags.debug = False  # Reset it back to the original as some tests will modify this in place.

    def test_get_timeline(self):
        mock_timeline = Mock()
        self.mock_driver.find_element.return_value = mock_timeline
        result = get_timeline(self.mock_driver)
        self.assertEqual(mock_timeline, result)
        self.mock_driver.find_element.assert_called_once_with(By.XPATH, "//div[@data-testid='primaryColumn']")

    def test_get_follow_sidebar(self):
        pass

    def test_take_element_screenshot(self):
        fake_screenshot_bytestring = b'\x89PNG\r\n\x1a\n'
        mock_element = Mock()
        mock_element.screenshot_as_png = fake_screenshot_bytestring
        result = take_element_screenshot(mock_element)
        self.assertEqual(result, fake_screenshot_bytestring)

    def test_take_element_screenshot_saves_to_file(self):
        self.flags.debug = True
        fake_screenshot_bytestring = b'\x89PNG\r\n\x1a\n'
        mock_element = Mock()
        mock_element.screenshot_as_png = fake_screenshot_bytestring
        result = take_element_screenshot(mock_element)
        self.assertEqual(result, fake_screenshot_bytestring)
        mock_element.screenshot.assert_called_once()

    def test_wait_for_page_load(self):
        pass

    def test_wait_for_page_load_failure(self):
        pass

    def test_load_more_tweets(self):
        pass

    def test_refresh_page(self):
        pass

    def test_search_promoted_tweet_in_timeline(self):
        pass

    def test_search_promoted_follow_in_sidebar(self):
        pass

    def test_get_promoted_author(self):
        pass

    def test_get_promoted_tweet_link(self):
        pass

    def test_get_promoted_tweet_official_link(self):
        pass

    def test_get_promoted_follow(self):
        pass

    def test_get_promoted_follow_link(self):
        pass


if __name__ == '__main__':
    main()
