import requests
import time
import json
import datetime
import os
import sys

class Helper:
    headers = None
    fileName = None

    @staticmethod
    def parseHTML(link):
        try:
            html = requests.get(link, headers = Helper.headers)
        except Exception, e:
            time.sleep(1)
            html = requests.get(link, headers = Helper.headers)
        return html.content

    @staticmethod
    def initialize(keyword):
        try:
            print '=== Starting Web Crawling ==='
            print 'Keyword: ' + keyword
            print '============================='

            Helper.keyword = keyword.lower()
            Helper.keyword = Helper.keyword.replace(' ', '+')

            with open('config.conf') as file:
                Helper.headers = json.load(file)
            file.close()
        except Exception, e:
            print '===== Error ======'
            print "You don't have config.conf file. Please read README.md!"
            sys.exit(3)

    @staticmethod
    def getEncodedKeyword():
        return Helper.keyword

    @staticmethod
    def createFileName():
        if Helper.fileName is None:
            now = datetime.datetime.now()
            directory = 'Results-Crawling/' + now.strftime("%Y%m%d%H%M%S")

            if not os.path.exists(directory):
                os.makedirs(directory)

            Helper.fileName = directory + '/customer_reviews.csv'
        return Helper.fileName
