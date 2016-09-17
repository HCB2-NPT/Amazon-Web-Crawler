from BeautifulSoup import BeautifulSoup
from ReviewsCrawler import ReviewsCrawler
from Helper import Helper

class ProductCrawler:
    url = ''
    keyword = ''

    def __init__(self, keyword):
        self.keyword = keyword.lower()
        self.keyword = keyword.replace(' ', '+')
        self.url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + keyword

    def checkMetadata(self, metadata):
        strs = self.keyword.lower()
        strs = strs.split('+')
        count = 0

        for str in strs:
            if str in metadata:
                count = count + 1

        return count > 1

    def verifyLink(self, link):
        flag = link.find('h5', {'class': 'a-spacing-none a-color-tertiary s-sponsored-list-header a-text-normal'})

        if flag is None:
            flag = True
            metadata = link.find('h2', {'class': 'a-size-medium a-color-null s-inline  s-access-title  a-text-normal'})

            if metadata is None:
                metadata = link.find('h2', {'class': 'a-size-medium a-color-null s-inline scx-truncate s-access-title  a-text-normal'})

                if metadata is not None:
                    metadata = metadata['data-attribute']
                    flag = self.checkMetadata(metadata.lower())
            else:
                metadata = metadata['data-attribute']
                flag = self.checkMetadata(metadata.lower())
        else:
            flag = False

        return flag

    def crawl(self):
        nextLink = self.url
        page = 1
        isCrawling = True

        while isCrawling:
            print '=== Parsing product - page ' + str(page) + ' ===='
            page = page + 1
            html = Helper.parseHMTL(nextLink)
            print html
            soup = BeautifulSoup(html)
            nextLink = soup.find('a', {'id': 'pagnNextLink'})
            productLinks = soup.findAll('li', {'class': 's-result-item celwidget'})

            for link in productLinks:
                if self.verifyLink(link):
                    productID = link['data-asin']
                    crawler = ReviewsCrawler(productID)
                    crawler.getReviews()

            if nextLink is None:
                isCrawling = False
            else:
                nextLink = 'https://www.amazon.com' + nextLink['href']

        print 'Done!'
