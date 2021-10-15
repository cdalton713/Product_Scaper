from pathlib import Path
from typing import List
from urllib.parse import urlparse, ParseResult


class Util:

    @staticmethod
    def file_to_urls(file_path: Path) -> List[ParseResult]:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        return [urlparse(_.split('\n')[0]) for _ in lines]


if __name__ == '__main__':
    print(Util.file_to_urls(Path('/Users/christiandalton/Github Projects/Product_Scaper/urls.txt')))