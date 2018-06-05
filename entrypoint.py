# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from scrapy.cmdline import execute


execute(['scrapy', 'crawl', 'blog_spider'])

