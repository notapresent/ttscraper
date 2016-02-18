import unittest
from mock import Mock, patch

from google.appengine.ext import testbed

from webclient import WebClient, login_form_data


class WebClientTestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()

        self.mock_session = Mock()
        self.mock_account = Mock(cookies=None)

    def tearDown(self):
        self.testbed.deactivate()

    def test_torrent_page_url_returns_correct_url(self):
        tid = 123456
        url = 'http://{}/forum/viewtopic.php?t={}'.format(WebClient.TRACKER_HOST, tid)
        wc = WebClient(self.mock_session)

        result = wc.torrent_page_url(tid)

        self.assertEqual(url, result)

    def test_get_torrent_page_calls_session(self):
        tid = 123456
        url = 'http://{}/forum/viewtopic.php?t={}'.format(WebClient.TRACKER_HOST, tid)

        wc = WebClient(self.mock_session)
        wc.get_torrent_page(tid)

        self.mock_session.get.assert_called_once_with(url)

    def test_get_torrent_page_returns_content(self):
        test_content = 'Test content'
        mock_response = Mock(text=test_content)
        self.mock_session.get = Mock(return_value=mock_response)

        wc = WebClient(self.mock_session)

        result = wc.get_torrent_page(0)
        self.assertEqual(result, test_content)

    def test_log_in_sets_cookies_from_account(self):
        test_cookies = {'testname': 'testvalue'}
        self.mock_account.cookies = test_cookies
        self.mock_session.cookies.update = Mock()

        wc = WebClient(self.mock_session, self.mock_account)
        wc.log_in()

        self.mock_session.cookies.update.assert_called_with(test_cookies)

    @patch('webclient.Account')
    def test_log_in_gets_account(self, mock_account_cls):
        wc = WebClient(self.mock_session)
        wc.log_in()

        mock_account_cls.get_one.assert_called_once_with()

    def test_log_in_sets_cookies_from_session(self):
        test_cookies = {'testname': 'testvalue'}
        self.mock_session.cookies = Mock(get_dict=Mock(return_value=test_cookies))

        wc = WebClient(self.mock_session, self.mock_account)
        wc.log_in()

        self.assertEqual(self.mock_account.cookies, test_cookies)

    def test_log_in_puts_saves_account(self):
        wc = WebClient(self.mock_session, self.mock_account)
        wc.log_in()

        self.mock_account.put.assert_called_once_with()

    def test_log_in_sends_request_if_no_cookies(self):
        wc = WebClient(self.mock_session, self.mock_account)
        wc.log_in()

        self.assertTrue(self.mock_session.post.called)

    def test_tracker_log_in_posts_to_correct_url(self):
        url = 'http://login.{}/forum/login.php'.format(WebClient.TRACKER_HOST)
        account_data = {'username': 'abc', 'password': 'abc', 'userid': 123456}
        mock_account = Mock(**account_data)
        correct_form_data = login_form_data(mock_account)
        mock_response = Mock(text='userid is {}'.format(account_data['userid']))
        self.mock_session.post = Mock(return_value=mock_response)

        wc = WebClient(self.mock_session, mock_account)
        wc.tracker_log_in()

        self.mock_session.post.assert_called_once_with(url, data=correct_form_data)

    def test_tracker_log_in_raises_if_failed(self):
        self.mock_session.post = Mock(return_value=Mock(text='some random text'))

        wc = WebClient(self.mock_session, self.mock_account)

        with self.assertRaises(RuntimeError):
            wc.tracker_log_in()

    def test_get_index_page_posts_to_correct_url(self):
        url = 'http://{}/forum/tracker.php'.format(WebClient.TRACKER_HOST)

        wc = WebClient(self.mock_session, self.mock_account)
        wc.get_index_page()

        self.mock_session.request.assert_called_once_with('POST', url, data=WebClient.INDEX_FORM_DATA)

    def test_get_index_page_returns_content(self):
        userid = 12345
        test_content = 'Test content {}'.format(userid)
        self.mock_account.cookies = {'somekey': 'somevalue'}
        self.mock_account.userid = userid
        mock_response = Mock(text=test_content)
        self.mock_session.request = Mock(return_value=mock_response)

        wc = WebClient(self.mock_session, self.mock_account)
        result = wc.get_index_page()

        self.assertEqual(result, test_content)

    def test_get_index_page_raises_if_cookie_login_failed(self):
        test_content = 'Content without userid'
        self.mock_account.cookies = {'somekey': 'somevalue'}
        self.mock_account.userid = 12345
        mock_response = Mock(text=test_content)
        self.mock_session.request = Mock(return_value=mock_response)

        wc = WebClient(self.mock_session, self.mock_account)

        with self.assertRaises(RuntimeError):
            result = wc.get_index_page()

    @patch('webclient.Account')
    def test_user_request_logs_in(self, mock_account_cls):
        wc = WebClient(self.mock_session)
        wc.user_request()

        mock_account_cls.get_one.assert_called_once_with()

    def test_user_request_calls_request(self):
        test_url = 'random text'

        wc = WebClient(self.mock_session, self.mock_account)
        wc.user_request(test_url)

        self.mock_session.request.assert_called_once_with(test_url)


class WebClientHelpersTestCase(unittest.TestCase):
    def test_login_form_data_returns_correct_data(self):
        account_data = {'username': 'abc', 'password': 'abc', 'userid': 123456}
        acc = Mock(**account_data)

        form_data = login_form_data(acc)

        self.assertEqual(form_data['login_password'], acc.password)
        self.assertEqual(form_data['login_username'], acc.username)
        self.assertTrue(form_data['login'])
