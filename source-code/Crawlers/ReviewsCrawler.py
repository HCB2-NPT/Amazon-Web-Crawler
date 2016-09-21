import time
import csv
from BeautifulSoup import BeautifulSoup
from Helper import Helper

class ReviewsCrawler:

    def __init__(self, productID):
        print '|\tProduct: ' + productID
        self.outputFile = Helper.createFileName()
        self.url = 'https://www.amazon.com/product-reviews/' + productID + '/?showViewpoints=0&sortBy=byRankDescending'
        html = Helper.parseHTML(self.url)
        self.links = self.getNumberOfLinks(html)
        self.expected = self.getExpectedReviews(html)
        print '|\t|\tPage(s): ' + str(self.links)
        print '|\t|\tCrawling'

    def getNumberOfLinks(self, html):
        soup = BeautifulSoup(html)
        pagelinks = soup.findAll('li', {'data-reftag': 'cm_cr_arp_d_paging_btm'})
        count = len(pagelinks)

        if count == 0:
            pagelinks = soup.findAll('div', {'class': 'a-section review'})
            if len(pagelinks) > 0:
                count = 1
        else:
            count = int(pagelinks[len(pagelinks) - 1].getText())

        return count

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

    def getExpectedReviews(self, html):
        soup = BeautifulSoup(html)
        total = soup.find('span', {'class': 'a-size-medium totalReviewCount'})
        return total.text

    def getExpected(self):
        return self.expected

    def getReviews(self):
        count = 0
        for page in range(1, self.links + 1):
            html = Helper.parseHTML(self.url + '&pageNumber=' + str(page))
            reviews = self.parseReviews(html)
            count = count +len(reviews)
            print '|\t|\t|\tPage ' + str(page) + ' has ' + str(len(reviews)) + ' reviews'
            for review in reviews:
                self.parseReview(review)
        return count
