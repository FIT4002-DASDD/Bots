"""
Testing scraping util functionality.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock, Mock, patch

from absl import flags
from selenium.webdriver.common.by import By

from bot.stages.scraping_util import get_timeline, load_more_tweets, take_element_screenshot, get_follow_sidebar, refresh_page, search_promoted_tweet_in_timeline, search_promoted_follow_in_sidebar, get_promoted_author, get_promoted_tweet_link, get_promoted_follow, get_promoted_follow_link, get_contents_and_likes

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
        mock_sidebar = Mock()
        self.mock_driver.find_element.return_value = mock_sidebar
        result = get_follow_sidebar(self.mock_driver)
        self.assertEqual(mock_sidebar, result)
        self.mock_driver.find_element.assert_called_once_with(By.XPATH, "//aside[@aria-label='Who to follow']")

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
    
    @patch('bot.stages.login.wait_for_page_load')
    def test_load_more_tweets(self, mock_wait_for_page_load):
        mock_wait_for_page_load.return_value = True
        load_more_tweets(self.mock_driver)
        self.mock_driver.execute_script.assert_called_once_with('window.scrollTo(0, document.body.scrollHeight);')

    @patch('bot.stages.login.wait_for_page_load')
    def test_refresh_page(self, mock_wait_for_page_load):
        mock_wait_for_page_load.return_value = True
        refresh_page(self.mock_driver)
        self.mock_driver.refresh.assert_called()

    def test_search_promoted_tweet_in_timeline(self):
        mock_timeline = Mock()
        search_promoted_tweet_in_timeline(mock_timeline)
        mock_timeline.find_element.assert_called_once_with(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[4]")
        
    def test_search_promoted_follow_in_sidebar(self):
        mock_sidebar = Mock()
        search_promoted_follow_in_sidebar(mock_sidebar)
        mock_sidebar.find_element.assert_called_once_with(By.XPATH, ".//*[contains(text(), 'Promoted')]//ancestor::div[5]")

    def test_get_promoted_author(self):
        mock_promoted_tweet = Mock()
        mock_promoter = Mock()
        mock_promoted_tweet.find_element.return_value = mock_promoter
        get_promoted_author(mock_promoted_tweet)
        mock_promoted_tweet.find_element.assert_called_once_with(By.XPATH, ".//*[contains(text(), '@')]")
        mock_promoter.get_attribute.assert_called_once_with('innerHTML')

    def test_get_promoted_tweet_link(self):
        pass

    def test_get_promoted_tweet_official_link(self):
        pass

    def test_get_promoted_follow(self):
        mock_promoted_follow = Mock()
        mock_promoter = Mock()
        mock_promoted_follow.find_element.return_value = mock_promoter
        get_promoted_follow(mock_promoted_follow)
        mock_promoted_follow.find_element.assert_called_once_with(By.XPATH, ".//*[contains(text(), '@')]")
        mock_promoter.get_attribute.assert_called_once_with('innerHTML')

    def test_get_promoted_follow_link(self):
        mock_promoted_follow = Mock()
        mock_link = Mock()
        mock_promoted_follow.find_element.return_value = mock_link
        get_promoted_follow_link(mock_promoted_follow)
        mock_promoted_follow.find_element.assert_called_once_with(By.XPATH, ".//a")
        mock_link.get_attribute.assert_called_once_with('href')

    def test_get_contents_and_likes(self):
        mock_contents_and_likes = Mock()
        self.mock_driver.find_elements_by_xpath.return_value = mock_contents_and_likes
        result = get_contents_and_likes(self.mock_driver)
        self.assertEqual(mock_contents_and_likes, result)
        self.mock_driver.find_elements_by_xpath.assert_called_once_with('//div[@data-testid="like"]//ancestor::div[4]/child::div[1]')
        


if __name__ == '__main__':
    main()
