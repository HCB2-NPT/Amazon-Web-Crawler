import requests
from BeautifulSoup import BeautifulSoup
from ReviewsCrawler import ReviewsCrawler

class ProductCrawler:
    url = ''
    keyword = ''
    headers = {}

    def __init__(self, keyword):
        self.keyword = keyword.lower()
        self.keyword = keyword.replace(' ', '+')
        self.url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + keyword
        self.setHeader()

    def setHeader(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            'Cookie': 'x-wl-uid=1ufpx359OBHL3vTgz/MbR7JgvkGJQRhz3LckdkNugbfHLCGPk7vetOZISd2oWd2WSJfsVdg2IorQ=; aws-session-id=160-6219495-6698944; aws-session-id-time=2102609170l; aws-ubid-main=158-6490660-4063723; s_pers=%20s_vnum%3D1474481169449%2526vn%253D1%7C1474481169449%3B%20s_invisit%3Dtrue%7C1471890969449%3B; session-token="GFYnOfaa8viObgPPKTFbjsjtj/hdS0xHe8XNxHlZ6bDpw/7cg59WOVThx4zcoPrv5qYG69uqL0Excw9ips2zxkJ/BZsdEYRMnlblx4vGeno59jEosFKNgWwelK2xxDUCyus3M8Sk+kb5jnJVHFfeBrN6g1Flud/Dn0YCpygq7J3MZSdA1GGRGS9DsL45rMKGSpXeKVdF0ObGtEfhUMXYlg=="; skin=noskin; session-id-time=2082787201l; session-id=164-0077019-9402407; ubid-main=191-7802258-0837316; csm-hit=6VXTHFXTYA2EXFZ39SK1+ba-BGZYQJSWFFZDKJGKWRY3-EZSZZ8EBJEJKAN8S6XHT|1473689714034'
        }

    def parseHMTL(self, url):
        html = requests.get(url, headers = self.headers)
        return html.content

    def crawl(self):
        nextLink = self.url
        page = 1
        isCrawling = True

        while isCrawling:
            print '=== Parsing product - page ' + str(page) + ' ===='
            page = page + 1
            html = self.parseHMTL(nextLink)
            soup = BeautifulSoup(html)
            nextLink = soup.find('a', {'id': 'pagnNextLink'})
            productLinks = soup.findAll('li', {'class': 's-result-item celwidget'})

            for link in productLinks:
                productID = link['data-asin']
                crawler = ReviewsCrawler(productID)
                crawler.getReviews()

            if nextLink is None:
                isCrawling = False
            else:
                nextLink = 'https://www.amazon.com' + nextLink['href']

        print 'Done!'
