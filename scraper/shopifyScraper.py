import traceback
from urllib.parse import ParseResult, urljoin

import requests

from scraper import Scraper
from util import ShopifyProduct


class ShopifyScraper(Scraper):
    def __init__(self, url: ParseResult):
        super().__init__()
        self.url = url
        self.products = self._get_products()
        pass

    def _get_products(self):
        page = 1
        count = 250
        p = {}
        while count == 250:
            resp = requests.get(
                urljoin(
                    f"{self.url.scheme}://{self.url.netloc}",
                    f"products.json?limit=250&page={page}",
                )
            )
            products = resp.json()["products"]
            for product in products:
                try:
                    item = ShopifyProduct(**product)
                    p[item.handle] = item
                except:
                    traceback.print_exc()
                    pass
            count = len(products)
            page += 1
        return p

    def get_product_by_url(self, url: ParseResult):
        handle = url.path.split("/")[-1]
        if handle in self.products:
            return self.products[handle]
        else:
            # TODO - some type of backup plan.  Possibly manual scraping as an absolute last resort.
            print("PRODUCT NOT FOUND")
