from unittest.mock import patch, call

from django.test import TestCase

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'starlest@gmail.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'starlest@gmail.com'
        })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['starlest@gmail.com'])

    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, mock_messages):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'starlest@gmail.com'
        })

        expected = "Check your email, we've sent you a link you can use to log in."
        self.assertEqual(mock_messages.success.call_args, call(response.wsgi_request, expected))


class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_creates_token_associated_with_email(self):
        self.client.post('/accounts/send_login_email', data={
            'email': 'starlest@gmail.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'starlest@gmail.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={
            'email': 'starlest@gmail.com'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
