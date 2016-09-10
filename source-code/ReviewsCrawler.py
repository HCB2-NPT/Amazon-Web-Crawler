import csv
import requests
from BeautifulSoup import BeautifulSoup

class ReviewsCrawler:
    url = ''
    links = 0
    outputFile = './amazon-reviews.csv'
    headers = {}

    def __init__(self, productID):
        print '--- Crawling Product: ' + productID +' ---'
        print 'Start Contructor'
        self.setHeader()
        self.url = 'https://www.amazon.com/product-reviews/' + productID + '/?showViewpoints=0&sortBy=byRankDescending'
        html = self.parseHTML(self.url)
        self.links = self.getNumberOfLinks(html)
        print 'Complete Contructor'

    def setHeader(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            'Cookie': 'x-wl-uid=1ufpx359OBHL3vTgz/MbR7JgvkGJQRhz3LckdkNugbfHLCGPk7vetOZISd2oWd2WSJfsVdg2IorQ=; aws-session-id=160-6219495-6698944; aws-session-id-time=2102609170l; aws-ubid-main=158-6490660-4063723; s_pers=%20s_vnum%3D1474481169449%2526vn%253D1%7C1474481169449%3B%20s_invisit%3Dtrue%7C1471890969449%3B; session-token="GFYnOfaa8viObgPPKTFbjsjtj/hdS0xHe8XNxHlZ6bDpw/7cg59WOVThx4zcoPrv5qYG69uqL0Excw9ips2zxkJ/BZsdEYRMnlblx4vGeno59jEosFKNgWwelK2xxDUCyus3M8Sk+kb5jnJVHFfeBrN6g1Flud/Dn0YCpygq7J3MZSdA1GGRGS9DsL45rMKGSpXeKVdF0ObGtEfhUMXYlg=="; session-id-time=2082787201l; session-id=164-0077019-9402407; ubid-main=191-7802258-0837316; csm-hit=J8ZWM3K7DF32THMS1ZQ4+s-WETX416M14AVQ4564431|1473531641764'
        }

    def getNumberOfLinks(self, html):
        soup = BeautifulSoup(html)
        pagelinks = soup.findAll('li', {'data-reftag': 'cm_cr_arp_d_paging_btm'})
        return len(pagelinks)

    def parseHTML(self, url):
        html = requests.get(self.url, headers = self.headers)
        return html.content

    def parseReviews(self, html):
        soup = BeautifulSoup(html)
        return soup.findAll('div', {'class': 'a-section review'})

    def parseReview(self, review):
        author = review.find('a', {'class': 'a-size-base a-link-normal author'})
        rating = review.find('span', {'class': 'a-icon-alt'})
        date = review.find('span', {'class': 'a-size-base a-color-secondary review-date'})
        content = review.find('span', {'class': 'a-size-base review-text'})

        if author is None:
            author = review.find('span', {'class': 'a-size-base a-color-secondary review-byline'})

        with open(self.outputFile, 'ab') as fp:
            file = csv.writer(fp, delimiter = ',',quoting=csv.QUOTE_MINIMAL)
            data = [
                str(author.text.encode('utf8')),
                str(rating.text[:3]),
                str(date.text[3:]),
                str(content.text.encode('utf8'))
            ]
            file.writerow(data)

    def getReviews(self):
        print 'Total ' + str(self.links) + ' page(s)'

        for page in range(1, self.links + 1):
            print 'Parsing page ' + str(page)
            html = self.parseHTML(self.url + '&pageNumber=' + str(page))
            reviews = self.parseReviews(html)
            print 'Total: ' + str(len(reviews)) + ' reviews'
            for review in reviews:
                self.parseReview(review)

        print '--- Crawling completed! ---'
