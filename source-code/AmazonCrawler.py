import sys
import getopt
from Crawlers import *

def main(argv):
    keyword = ''

    try:
        opts, args = getopt.getopt(argv,"hk:",["keyword="])
    except getopt.GetoptError:
        print 'AmazonCrawler.py -k <keyword>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'AmazonCrawler.py -k <keyword>'
            sys.exit()
        elif opt in ("-k", "--keyword"):
            keyword = arg

    crawler = ProductCrawler(keyword)
    crawler.crawl()

if __name__ == '__main__':
    main(sys.argv[1:])