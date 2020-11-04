import argparse
from scrap import KyoboScraper

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="""
        parse yes24 search parameters
        """)

    parser.add_argument('--key', type=str, required=True, help="""
        enter the key-link you want to search for
        """)

    parser.add_argument('--pages', type=int, required=True, help="""
        enter the pages of you want to search for
        """)

    parser.add_argument('--name', type=str, required=True, help="""
            enter the name of you want to save for
            """)
    return vars(parser.parse_args())

if __name__ == "__main__":

    search_keys = parse_command_line_args()

    Scraper = KyoboScraper(**search_keys)
    links = Scraper.scrap_links()
    Scraper.scrap_books(links)


