import traceback
from urllib.parse import ParseResult, urljoin
import requests
import json
from scraper import Scraper
from util import WooProduct, WooVariant
from bs4 import BeautifulSoup


class WooScraper(Scraper):
    def __init__(self, url: ParseResult):
        super().__init__()
        self.url = url
        self.products = self._get_products()
        pass

    def _get_products(self):
        resp = requests.get(
            urljoin(f"{self.url.scheme}://{self.url.netloc}", self.url.path)
        )
        soup = BeautifulSoup(resp.content, "html.parser")

        handle = self.url.path.split("/")[-1]
        product_title = soup.find(class_="product_title").text

        products_variation_form = soup.find(class_="variations_form cart")
        form_data = products_variation_form.get("data-product_variations")
        form_data = json.loads(form_data)

        p = {}
        variants = []

        for variant in form_data:
            try:
                item = WooVariant(**variant)
                variants.append(item)
            except:
                traceback.print_exc()
                pass

        p[handle] = WooProduct(title=product_title, variants=variants, handle=handle)

        return p

    def get_product_by_url(self, url: ParseResult):
        handle = url.path.split("/")[-1]
        if handle in self.products:
            return self.products[handle]
        else:
            # TODO - some type of backup plan.  Possibly manual scraping as an absolute last resort.
            print("PRODUCT NOT FOUND")
