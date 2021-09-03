# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time

from pprint import pprint


class MVideo:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
        self.driver.get('https://www.mvideo.ru')
        self.close_popup()

    def close_popup(self):
        time.sleep(3)
        actions = ActionChains(self.driver)
        actions.move_by_offset(100, 100).click()
        actions.perform()

    def __get_gallery_products(self, section):
        goods = []
        temp_goods = {}
        while True:
            try:
                time.sleep(3)
                products = self.__getProducts(section)
                result = {i['img']: i for i in products if i['price'] != ''}
                temp_goods.update(result)
                btn_next_xpath = './/a[contains(@class, "next-btn c-btn c-btn_scroll-horizontal ' \
                                 'c-btn_icon i-icon-fl-arrow-right")]'
                btn_next = 'a[class="next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right"]'
                btn = section.find_element_by_xpath(btn_next_xpath)
                WebDriverWait(section, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_next)))
                btn.click()
            except exceptions.TimeoutException:
                goods.extend(temp_goods.values())
                break
        return goods

    def __move_to_element(self, el):
        actions = ActionChains(self.driver)
        actions.move_to_element(el)
        actions.perform()

    def get_goods_by_category_title(self, category_name):
        section_xpath = "//h2[contains(@class, 'u-hidden-phone') and contains(text(), '" + category_name + "')]" \
                        "/ancestor::div[contains(@class,  'section')]"
        section = self.driver.find_element_by_xpath(section_xpath)
        self.__move_to_element(section)
        return self.__get_gallery_products(section)

    def __getProducts(self, section):
        products = []
        product_xpath = ".//li[contains(@class, 'gallery-list-item')]"
        products_xpath = section.find_elements_by_xpath(product_xpath)
        for product in products_xpath:
            item = self.__getProduct(product)
            products.append(item)

        return products

    def __getProduct(self, product):
        return {
            'title': product.find_element_by_xpath(
                ".//h3[contains(@class, 'fl-product-tile-title')]").text,
            'price': product.find_element_by_xpath(".//span[contains(@class, 'fl-product-tile-price__current')]").text,
            'img': product.find_element_by_xpath(
                ".//img[contains(@class, 'lazy product-tile-picture__image')]").get_attribute('src')
        }
