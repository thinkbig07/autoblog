# -*- coding: utf-8 -*-
import re
import traceback

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
            url_key = None
            lei_phone_url = reduce(lambda x, y: x +"/" + y, response.url.split("/")[:-1]) + '/' + response.url.split("/")[-1].split("=")[-1] + '.html'
            xue_qiu_url = response.url.replace(response.url.split("//")[0], 'http:', 1)
            if response.url in category_posts.keys():
                url_key = response.url
            elif lei_phone_url in category_posts.keys():
                url_key = lei_phone_url
            elif xue_qiu_url in category_posts.keys():
                url_key = xue_qiu_url

            if url_key:
                try:
                    item['title'] = category_posts[url_key]['title']
                    item['date'] = category_posts[url_key]['date']
                    item['categories'] = category_posts[url_key]['categories']
                    item['tags'] = category_posts[url_key]['tags']
                    item['desc'] = category_posts[url_key]['desc']
                    item['url'] = response.url
                    yield self.exact_contents(response, item, tags_mapping)
                except:
                    traceback.print_exc()

    def html_to_md(self, html_content):
        return self.convert_img(tomd.convert(html_content))

    def convert_img(self, md_content_with_img_tags):
        try:
            regex_str = r'''<img(.*)>'''
            regex = re.compile(regex_str)

            replace_regex_str = r'''src=\"(.*?)\"'''
            replace_regex = re.compile(replace_regex_str)
            replace_url = re.findall(replace_regex, md_content_with_img_tags)
            for img_url in replace_url:
                replace_content = r'''![](%s)''' % img_url
                md_content_with_img_tags = re.sub(regex, replace_content, md_content_with_img_tags, 1)
            return md_content_with_img_tags
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


