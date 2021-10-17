"""
Testing interact functionality.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock, patch, Mock

from bot.stages.interact import agree_to_policy_updates_if_exists, retweet_posts, visit_account


class InteractTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up code artifacts to be used for testing across all tests.
        @note: runs only once for each test class as opposed to setUp()
        :return:
        """
        pass

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

    def tearDown(self) -> None:
        """
        Tears down code artifacts used for testing created in the setUp().
        :return:
        """
        self.mock_driver = None

    def test_interact(self):
        pass

    def test_agree_to_policy_updates_if_exists(self):
        self.mock_driver.find_element_by_xpath.return_value = None
        result = agree_to_policy_updates_if_exists(self.mock_driver)
        self.assertEqual(None, result)
        self.mock_driver.find_element_by_xpath.assert_called_once_with(
            "//div[@role='dialog']")

    @patch('bot.stages.bot_info.get_bot')
    @patch('bot.stages.interact.visit_account', return_value=True)
    @patch('bot.stages.interact.like_post', return_value=None)
    def test_retweet_posts(self, mock_get_bot, mock_visit_account, mock_like_post):
        username = 'Melinda06678369'
        mock_tweet = Mock()
        mock_get_bot.return_value = ['@democracynow', '@IlhanMN']
        self.mock_driver.find_elements_by_xpath.return_value = [mock_tweet]
        result = retweet_posts(self.mock_driver, username)
        self.mock_driver.find_elements_by_xpath.assert_called_with(
            '//div[@data-testid="retweet"]')
        self.mock_driver.find_element_by_xpath.assert_called_with(
            '//div[@data-testid="retweetConfirm"]')
        self.assertEqual(None, result)

    def test_visit_account(self):
        visit_account(self.mock_driver, '@SkyNews')
        self.mock_driver.get.assert_called_with('https://twitter.com/@SkyNews')


if __name__ == '__main__':
    main()
