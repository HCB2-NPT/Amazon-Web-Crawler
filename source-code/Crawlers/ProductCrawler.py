from BeautifulSoup import BeautifulSoup
from ReviewsCrawler import ReviewsCrawler
from Helper import Helper

class ProductCrawler:

    def __init__(self):
        self.url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + Helper.getEncodedKeyword()

    def checkMetadata(self, metadata):
        strs = Helper.getEncodedKeyword()
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
            flag = self.checkMetadata(self.getContentLink(link).lower())
        else:
            flag = False

        return flag

    def getContentLink(self, link):
        metadata = link.find('h2', {'class': 'a-size-medium a-color-null s-inline  s-access-title  a-text-normal'})

        if metadata is None:
            metadata = link.find('h2', {'class': 'a-size-medium a-color-null s-inline scx-truncate s-access-title  a-text-normal'})

            if metadata is not None:
                metadata = metadata['data-attribute']
        else:
            metadata = metadata['data-attribute']

        return metadata

    def crawl(self):
        nextLink = self.url
        page = 1
        isCrawling = True

        while isCrawling:
            print 'Result page ' + str(page)
            page = page + 1
            html = Helper.parseHTML(nextLink)
            soup = BeautifulSoup(html)
            nextLink = soup.find('a', {'id': 'pagnNextLink'})
            productLinks = soup.findAll('li', {'class': 's-result-item celwidget'})

            for link in productLinks:
                if self.verifyLink(link):
                    productID = link['data-asin']
                    crawler = ReviewsCrawler(productID)
                    actual = crawler.getReviews()
                    expected = crawler.getExpected()
                    contentLink = self.getContentLink(link)
                    Helper.writeLog([
                        productID,
                        contentLink,
                        expected,
                        actual
                    ])

            if nextLink is None:
                isCrawling = False
            else:
                nextLink = 'https://www.amazon.com' + nextLink['href']

        print '=== Done! ==='
