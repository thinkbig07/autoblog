# -*- coding: utf-8 -*-
import re
import scrapy
import tomd
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from autoblog.spiders.sites.bluereader import all_posts
from autoblog.tools.log_processor import logger
from autoblog.spiders.sites import tags_contents_mapping
from autoblog.items import AutoblogItem


class BlogSpider(scrapy.Spider):
    name = "blog_spider"

    start_urls = []
    for category_posts in all_posts:
        for posts in category_posts.keys():
            start_urls.append(posts)
    logger.info(start_urls)

    def parse(self, response):
        item = AutoblogItem()
        tags_mapping = tags_contents_mapping
        for category_posts in all_posts:
            if response.url in category_posts.keys():
                try:
                    item['title'] = category_posts[response.url]['title']
                    item['date'] = category_posts[response.url]['date']
                    item['categories'] = category_posts[response.url]['categories']
                    item['tags'] = category_posts[response.url]['tags']
                    item['desc'] = category_posts[response.url]['desc']
                    item['url'] = response.url.replace(response.url.split("//")[0], 'http:', 1)
                    yield self.exact_contents(response, item, tags_mapping)

                except:
                    logger.exception('parse error', exc_info=True)

    def html_to_md(self, html_content):
        return self.convert_img(tomd.convert(html_content))

    def convert_img(self, md_content_with_img_tags):
        try:
            regex_str = r'''<img(.*)>'''
            regex = re.compile(regex_str)

            replace_regex_str = r'''src=\"(.*?)\"'''
            replace_regex = re.compile(replace_regex_str)
            replace_url = re.search(replace_regex, md_content_with_img_tags).group(1)
            replace_content = r'''![](%s)''' % replace_url

            return re.sub(regex, replace_content, md_content_with_img_tags)
        except:
            return md_content_with_img_tags

    def to_string(self, unknown_content):
        if isinstance(unknown_content, list):
            str = ''
            for item in unknown_content:
                str += item
            return str
        else:
            return unknown_content

    def exact_contents(self, response,item,tags_contents_mapping):
        if item['tags'] not in tags_contents_mapping.keys():
            return
        inner_content = response.selector.xpath(tags_contents_mapping[str(item['tags'])][1]).extract()
        item['contents'] = self.html_to_md(self.to_string(inner_content))
        return item


