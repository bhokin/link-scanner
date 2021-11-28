import sys
import urllib.error
import urllib.request

from typing import List
from selenium import webdriver
from urllib.error import HTTPError, URLError
from selenium.webdriver.chrome.options import Options


def get_links(url: str) -> List:
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """

    url_list = []
    browser.get(url)
    elements = browser.find_elements_by_tag_name("a")
    for link in elements:
        url: str = link.get_attribute('href')
        if url is not None:
            if '#' in url:
                url = url.split('#')[0]
            elif '?' in url:
                url = url.split('?')[0]
            if url not in url_list:
                url_list.append(url)

    return url_list


def is_valid_url(url: str):
    """Return True if the URL is OK, False otherwise. Also return False is the URL has invalid syntax."""

    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError as er:
        if er.getcode() == 403:
            return True
        return False
    else:
        return True


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.
    """
    in_valid_urls = []
    for url in urllist:
        if not is_valid_url(url):
            in_valid_urls.append(url)
    return in_valid_urls


if __name__ == '__main__':
    try:
        the_urls = sys.argv[1]
    except IndexError:
        print('Usage:  python3 link_scan.py url')
        print('\nTest all hyperlinks on the given url.')
    else:
        my_options = Options()
        my_options.headless = True
        browser = webdriver.Chrome(executable_path='C:/Users/Administratorz/Downloads/chromedriver.exe',
                                   options=my_options)
        urls = get_links(the_urls)
        for each_url in urls:
            print(each_url)

        bad_urls = invalid_urls(urls)

        print('\nBad Links:')
        for bad_url in bad_urls:
            print(bad_url)
