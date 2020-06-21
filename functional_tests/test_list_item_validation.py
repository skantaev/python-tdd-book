from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Эдит отправляется на домашнюю страницу и случайно пытается добавить пустой элемент
        # списка. Она нажимает enter в пустом инпутбоксе
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер прерывает запрос и не дает загрузить страницу списка
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # Она начинает вводить текст для нового элемента и ошибка пропадает
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))

        # И добавление происходит успешно
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Уже намеренно она решает добавить пустой элемент списка во второй раз
        self.get_item_input_box().send_keys(Keys.ENTER)

        # И снова бразуер не уступает
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:invalid'))

        # И может исправить это, введя туда какой-нибудь текст
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector('#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        # Эдит отправляется на домашнюю страницу и создает новый список
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # Случайно она пытается ввести снова тот же элемент
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Она видит полезное сообщение об ошибке
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector('.has-error').text,
                "You've already got this in your list",
            )
        )
