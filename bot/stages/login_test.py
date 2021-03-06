"""
Testing login functionality.
"""
from unittest import TestCase, main
from unittest.mock import MagicMock, patch, Mock

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bot.stages.login import login_or_die, alternate_screen_login, verify_phone_number


class LoginTest(TestCase):
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

    def test_login_failure_quits_webdriver(self):
        self.mock_driver.get.side_effect = Exception()
        with self.assertRaises(Exception):
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

    def test_alternate_screen_login(self):
        username = 'fakeusername'
        password = 'fakepassword'
        mock_username = Mock()
        mock_password = Mock()
        self.mock_driver.find_element_by_name.return_value = mock_username
        self.mock_driver.find_element.return_value = mock_password
        alternate_screen_login(self.mock_driver, username, password)
        self.mock_driver.find_element_by_name.assert_called_once_with('username')
        self.mock_driver.find_element.assert_called_once_with(By.NAME, 'password')
        mock_username.send_keys.assert_called_with(Keys.RETURN)
        mock_password.send_keys.assert_called_with(Keys.RETURN)

    @patch('bot.stages.bot_info.get_bot')
    def test_verify_phone_number(self, mock_get_bot):
        mock_get_bot.return_value = "+61404245906"
        mock_phone_element = Mock()
        self.mock_driver.find_element_by_name.return_value = mock_phone_element
        verify_phone_number(self.mock_driver, 'ElizaHahns')
        xpath = "//strong[contains(text(), 'Your phone number ends in 06')]"
        self.mock_driver.find_element_by_xpath.assert_called_with(xpath)
        self.mock_driver.find_element_by_name.assert_called_with('challenge_response')
        mock_phone_element.send_keys.assert_any_call("+61404245906")
        mock_phone_element.send_keys.assert_any_call(Keys.RETURN)


if __name__ == '__main__':
    main()
