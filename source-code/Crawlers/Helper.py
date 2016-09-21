import requests
import time
import json
import datetime
import os
import sys
import csv

class Helper:
    headers = None
    fileName = None
    fileStatistic = None

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
            Helper.fileStatistic = directory + '/statistic.csv'

            with open(Helper.fileStatistic, 'ab') as fp:
                file = csv.writer(fp, delimiter = ',',quoting=csv.QUOTE_MINIMAL)
                data = [
                    'Product ID',
                    'Product Name',
                    'Expected',
                    'Actual'
                ]
                file.writerow(data)

        return Helper.fileName

    @staticmethod
    def writeLog(data):
        with open(Helper.fileStatistic, 'ab') as fp:
            file = csv.writer(fp, delimiter = ',',quoting=csv.QUOTE_MINIMAL)
            file.writerow(data)
