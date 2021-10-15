from abc import ABC
from typing import Tuple
from urllib.parse import ParseResult
from urllib.parse import urljoin, urlparse
from seleniumwire import webdriver
import requests


class Scraper(ABC):
    def __init__(self):
        self.url = None
        self.products = None

    @staticmethod
    def _test_shopify(url: ParseResult) -> Tuple[bool, ParseResult]:
        resp = requests.get(urljoin(f'{url.scheme}://{url.netloc}', 'products.json?limit=10'))

        if resp.status_code == 200:
            return True, url

        # Check if the site is using shopify on the hidden in the backend.  A request will be sent with 'myshopify'
        # in the url name which is Shopify's constant, 'hidden' url for their store.

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(urljoin(f'{url.scheme}://{url.netloc}', url.path))
        for request in driver.requests:
            if 'myshopify' in request.url:
                return True, urlparse(request.url)

        return False, urlparse('')

    @staticmethod
    def factory(url: ParseResult):
        # Determine what type of ecommerce site the website is.  ie. Shopify, BigCommerce, WooCommerce, etc.
        site_type, url_ = Scraper._test_shopify(url)

        #  SHOPIFY
        if site_type:
            from scraper.shopifyScraper import ShopifyScraper
            return ShopifyScraper(url_)

    #     if BIGCOMMERCE
    #     if WooCommerce
    #     ...

    def _get_products(self):
        raise NotImplementedError

    def get_product_by_url(self, url: ParseResult):
        raise NotImplementedError
