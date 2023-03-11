#./subfinder -d microsoft.com | httpx | python3 getwapp.py


import sys
from Wappalyzer import Wappalyzer, WebPage
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from urllib3.exceptions import MaxRetryError

def main():
    # Get the list of URLs from an argument or stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            urls = f.read().splitlines()
    else:
        urls = sys.stdin.read().splitlines()

    # Initialize Wappalyzer
    wappalyzer = Wappalyzer.latest()

    # Collect information for each URL
    for url in urls:
        try:
            webpage = WebPage.new_from_url(url, timeout=5)
            info = wappalyzer.analyze(webpage)
            print(f'{url}: {info}')
        except MaxRetryError as e:
            pass
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
