# -*- coding: utf-8 -*-

import re
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from autoblog.spiders.sites import BlueReaderAccount
from autoblog.tools.log_processor import logger
from autoblog.tools.login_api import SharedAPI, SiteUrlEnum
from autoblog.tools.timestamp_converter import TimeConverter


class BlueReader(SharedAPI):
    def __init__(self, username, password):
        super(BlueReader,self).__init__()
        self.token = self.get_blue_reader_token(username, password)

    def get_category_name_id(self):
        categories_list = []
        content = self.s.get(SiteUrlEnum.BLUE_READER).content
        category_str = r'''a data-categoryId="(.*?)" data-title="(.*?)"'''
        category_regex = re.compile(category_str)
        for item in category_regex.findall(content):
            d = dict()
            d["category_title"] = item[1].decode('utf-8')
            d["category_id"] = item[0]
            categories_list.append(d)
        return categories_list

    def get_posts_by_category(self, category_dict):
        post_info = dict()
        parm = {'do':'action', 'act':'rssarticles'}
        data = {'rssId':'undefined', 'categoryId':category_dict["category_id"],'lastPubDate':0,\
                'lastId':0, 'token':self.token, 'isStar':'undefined', 'noClean':0,\
                'keywords':'', 'isTodayHot':'undefined','onlyUnread':2, 'translate':0}
        try:
            request_data = self.s.post(SiteUrlEnum.BLUE_READER + '/index.php', params=parm, data=data).json()["data"]
            if request_data:
                request_data = request_data[0]
                for item in request_data["articles"]:
                    article = dict()
                    article['title'] = item['title']
                    article['date'] = TimeConverter.timestamp_to_md_format(request_data["articles"][0]['pubDate'])
                    article['tags'] = item['rssTitle']
                    article['categories'] = category_dict["category_title"]
                    article['desc'] = item['desc']
                    post_info[item['link']] = article
        except:
            traceback.print_exc()
            # logger.error('get token failed', exc_info=True)
        return post_info

    def get_all_posts(self):
        return_list = []
        for item in self.get_category_name_id():
            return_list.append(self.get_posts_by_category(item))
        return return_list


blue_reader = BlueReader(BlueReaderAccount["username"], BlueReaderAccount["password"])
all_posts = blue_reader.get_all_posts()
