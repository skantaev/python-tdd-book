from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Эдит отправляется на крутой сайт с суперсписками и замечает секцию "Войти" в навбаре
        # в первый раз. Там требуется ввести свой адрес эл. почты, что она и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Возникает сообщение, которое сообщает ей, что письмо было отослано
        self.wait_for(
            lambda: self.assertIn(
                'Check your email', self.browser.find_element_by_tag_name('body').text
            )
        )

        # Она проверяет свою эл. почту и находит там сообщение
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # В нем есть ссылка
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Она нажимает на нее
        self.browser.get(url)

        # и она вошла!
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # Теперь она выходит
        self.browser.find_element_by_link_text('Log out').click()

        # Она вышла
        self.wait_to_be_logged_out(email=TEST_EMAIL)