import traceback
from pathlib import Path
from util import Util
from scraper import Scraper
import logging
from typing import List
from util import ShopifyProduct
import json

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def print_results(res: List[ShopifyProduct]):
    r = {}
    for result in res:
        r[result.title] = {}
        for variant in result.variants:
            r[result.title][variant.title] = variant.price
    print(json.dumps(r, indent=4, sort_keys=True))


if __name__ == '__main__':
    site_urls = Util.file_to_urls(Path('urls.txt'))

    domains = {}
    results = []
    for site_url in site_urls:
        try:
            logger.warning("Scraping Site:\t{}\tHandle:\t{}".format(site_url.netloc, site_url.path))
            if site_url.netloc in domains:
                scraper = domains[site_url.netloc]
            else:
                scraper = Scraper.factory(site_url)
                domains[site_url.netloc] = scraper

            results.append(scraper.get_product_by_url(site_url))

        except Exception as e:
            traceback.print_exc()

    print_results(results)
