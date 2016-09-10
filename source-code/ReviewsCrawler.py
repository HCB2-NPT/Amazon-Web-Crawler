import urllib
import csv
import requests
from BeautifulSoup import BeautifulSoup

class ReviewsCrawler:
    url = ''
    links = 0
    proxy = '169.50.87.252:80'
    outputFile = './amazon-reviews.csv'
    session = requests.Session()

    def __init__(self, productID):
        print 'Start Contructor'
        self.url = 'https://www.amazon.com/product-reviews/' + productID + '/?showViewpoints=0&sortBy=byRankDescending'
        html = self.parseHTML(self.url)
        self.links = self.getNumberOfLinks(html)
        print 'Complete Contructor'

    def getNumberOfLinks(self, html):
        soup = BeautifulSoup(html)
        pagelinks = soup.findAll('li', {'data-reftag': 'cm_cr_arp_d_paging_btm'})
        return len(pagelinks)

    def parseHTML(self, url):
        html = requests.get(url, proxies={"http": self.proxy})
        return html.content

    def parseReviews(self, html):
        soup = BeautifulSoup(html)
        return soup.findAll('div', {'class': 'a-section review'})

    def parseReview(self, review):
        author = review.find('a', {'class': 'a-size-base a-link-normal author'})
        rating = review.find('span', {'class': 'a-icon-alt'})
        date = review.find('span', {'class': 'a-size-base a-color-secondary review-date'})
        content = review.find('span', {'class': 'a-size-base review-text'})

        with open(self.outputFile, 'ab') as fp:
            file = csv.writer(fp, delimiter = ',',quoting=csv.QUOTE_MINIMAL)
            data = [str(author.text.encode('utf8')), str(rating.text[:3]), str(date.text[3:]), str(content.text.encode('utf8'))]
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
            print 'Parsing completed!'

crawler = ReviewsCrawler('B0002E1P08')
crawler.getReviews()