"""
Testing interact functionality.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock

from bot.stages.interact import interact, agree_to_policy_updates_if_exists, like_post, retweet_posts, visit_account


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
        pass

    def test_like_post(self):
        pass

    def test_retweet_posts(self):
        pass

    def test_visit_account(self):
        pass


if __name__ == '__main__':
    main()
