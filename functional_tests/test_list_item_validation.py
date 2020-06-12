from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

MAX_WAIT = 10


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Эдит отправляется на домашнюю страницу и случайно пытается добавить пустой элемент
        # списка. Она нажимает enter в пустом инпутбоксе
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и там появляется сообщение об ошибке: "элементы списка
        # не могут быть пустыми"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item",
        ))

        # Она пробует еще раз с заполненным текстом, и теперь все работает
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Уже намеренно она решает добавить пустой элемент списка во второй раз
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Она получает то же предупреждение на странице списка
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item",
        ))

        # И может исправить это, введя туда какой-нибудь текст
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
