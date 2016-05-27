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
    html = scraperwiki.scrape(url, user_agent='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
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

