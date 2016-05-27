import scrapy
from scrapy.crawler import CrawlerProcess
import scraperwiki
from datetime import datetime
from urlparse import urljoin
import lxml.html
import dateutil.parser
from urllib2 import HTTPError
import time
def parse_page(url):
    html = ""
    max_retry = 10
    print url
    for i in range(max_retry):
        try:
            html = scraperwiki.scrape(url)
            break
        except HTTPError:
            print "error"
            if i + 1 == max_retry:
                raise
            else:
                print "retrying"
                time.sleep(10)
    root = lxml.html.fromstring(html)
    table = root.xpath('//table[@class=\'shrs_s1\']')[0]
    header_texts = table.xpath('.//td[@class=\'shrs_s2\']/text()')
    date_str = header_texts[-1].strip()[1:-1]
    date = dateutil.parser.parse(date_str)
    number_texts = table.xpath('.//td[contains(@style, \'right\')]/text()')
    numbers = [int(s.replace(',', '').replace('$', '').strip()) for s in number_texts]
    d = {'date': date, 
            'today_mainland_admission': numbers[0],
            'today_local_admission':numbers[1],
            'today_total_admission':numbers[2],
            'today_highest_price': numbers[3],
            'today_lowest_price': numbers[4],
            'today_average_price': numbers[5],
            'tomorrow_mainland_admission': numbers[6],
            'tomorrow_local_admission': numbers[7],
            'tomorrow_total_admission': numbers[8],
            }
    print d
    scraperwiki.sqlite.save(unique_keys=['date'], data=d)
parse_page("http://www.fehd.gov.hk/tc_chi/sh/data/supply_tw.html")

