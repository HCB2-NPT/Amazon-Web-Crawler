# Amazon-Web-Crawler
Course: Data Mining
Project: 7 - Web Crawling
Version: 1.3

## Environment
* Development on OS: Ubuntu 16.04 TLS
* Programming language: Python 2.7.12

## Dependency packages:
* requests
* BeautifulSoup 3
 
## Usage
```bash
cd source-code
# python AmazonCrawler.py -k <keyword>
python AmazonCrawler.py -k "Sony Speaker Ultra Portable"
```

## Config

```
{
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": AMAZON-COOKIE
    "Host": "www.amazon.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
}
```

**Note:** Create file "config.conf" in root folder.

## Structure

```
source-code
|   AmazonCrawler.py
|   config.conf
|
└───Crawlers
|   |    __init__.py
|   |    Helper.py
|   |    ProductCrawler.py
|   |    ReviewsCrawler.py
|
└───Results-Crawling
    └───yyyymmddhhMMss
    |    |    customer_reviews.csv
    |
    └───...
```
