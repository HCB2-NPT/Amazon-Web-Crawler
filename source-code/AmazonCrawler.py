import sys
import getopt
from Crawlers import *

def main(argv):
    keyword = ''

    try:
        opts, args = getopt.getopt(argv,"hvk:",["keyword="])
    except getopt.GetoptError:
        print 'AmazonCrawler.py -k <keyword>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'AmazonCrawler.py -k <keyword>'
        elif opt == '-v':
            print "15HCB2 Team NPT - Amazon Web Crawler 1.2"
        elif opt in ("-k", "--keyword"):
            keyword = arg
            Helper.initialize(keyword)
            crawler = ProductCrawler()
            crawler.crawl()

    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])