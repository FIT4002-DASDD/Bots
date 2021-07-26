"""
Testing login functionality.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from bot.stages.login import login_or_die


class LoginTest(TestCase):
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

    def test_login_failure_is_fatal(self):
        self.mock_driver.get.side_effect = Exception()
        login_or_die(self.mock_driver, '', '')
        self.mock_driver.quit.assert_called_once()

    @patch('selenium.webdriver.support.ui.WebDriverWait')
    @patch('selenium.webdriver.support.expected_conditions.visibility_of_element_located')
    @patch('bot.stages.login.wait_for_page_load')
    def test_login_success(self, mock_webdriver_wait, mock_ec, mock_page_load_fn):
        username = 'fakeusername'
        password = 'fakepassword'
        mock_page_load_fn.return_value = True

        login_or_die(self.mock_driver, username, password)
        self.mock_driver.quit.assert_not_called()


if __name__ == '__main__':
    main()
