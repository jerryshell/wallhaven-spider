import re
import time

import requests
import requests.exceptions
from bs4 import BeautifulSoup

from spider_random.spider_lib import log_print
from spider_random.task import Task


class SpiderWallhaven():
    """
    wallhaven 爬虫

    属性：
        url: 首页 URL
        download_task_center: 下载任务中心
        home_page_image_links_set: 首页的图片链接集合
    """

    def __init__(self, home_page_url, download_task_center):
        self.home_page_url = home_page_url
        self.download_task_center = download_task_center
        self.home_page_image_links_set = set()

    def analysis_home_page(self):
        """
        分析网站主页
        :return: None
        """
        log_print('正在请求网站首页 ...')
        home_page_res = requests.get(self.home_page_url)
        home_page_res.encoding = 'utf-8'
        log_print('正在分析网站首页 ...')
        home_page_soup = BeautifulSoup(home_page_res.text, 'html.parser')
        home_page_image_tags = home_page_soup.select('.thumb-listing-page a')

        log_print('正在将首页的图片标签添加到集合 ...')
        for i in home_page_image_tags:
            img_link = i.get('href')
            re_result = re.match(r'https.*/\d+', img_link)
            if re_result:
                self.home_page_image_links_set.add(re_result.group().rstrip('/'))
        log_print('首页分析完成')

    def handle_home_page_image_links_set(self):
        """
        处理首页的图片链接集合
        :return:
        """
        count = 0
        for image_detail_link in self.home_page_image_links_set:
            count += 1
            log_print('=-= 处理第 %s 个图片详情页面 =-=' % count)
            self.analysis_image_detail_page(image_detail_link)
            time.sleep(2)

    def analysis_image_detail_page(self, image_detail_link):
        """
        分析图片详情页面，然后将图片信息封装成任务投送任务中心
        :param image_detail_link: 图片详情页面链接
        :return: None
        """
        try:
            log_print('正在请求图片详情页面 ... %s' % image_detail_link)
            image_detail_page_res = requests.get(image_detail_link, timeout=5)
            image_detail_page_res.encoding = 'utf-8'
            log_print('正在分析图片详情页面 ...')
            image_detail_page_soup = BeautifulSoup(image_detail_page_res.text, 'html.parser')
            image_tag = image_detail_page_soup.select('#wallpaper')
            image_name = image_tag[0]['src'].split('/')[-1]
            image_url = 'https:' + image_tag[0]['src'].strip()
            log_print('图片详情页面分析完成\nImage:\t%s\nURL:\t%s' % (image_name, image_url))
            new_task = Task(image_name, image_url)
            self.download_task_center.add_task(new_task)
            log_print('已将图片信息封装并投送任务中心')
        except requests.exceptions.Timeout as e:
            log_print(e)
            log_print('!! 连接超时，该图片跳过 !!')
        except requests.exceptions.SSLError as e:
            log_print(e)
            log_print('!! 网络错误，该图片跳过 !!')
        except requests.exceptions.ConnectionError as e:
            log_print(e)
            log_print('!! 网络错误，该图片跳过 !!')
        except IndexError as e:
            log_print(e)
            log_print('image_tag: %s' % image_tag)
            log_print('!! 网页错误，该图片已跳过 !!')

    def page_analyze_complete(self):
        """
        页面分析完成，开始驱动下载器
        :return: None
        """
        self.download_task_center.drive_downloader()
        log_print('页面分析完成 --- 开始驱动下载器')

    def run(self):
        """
        爬虫入口
        :return: None
        """
        self.analysis_home_page()
        self.handle_home_page_image_links_set()
        self.page_analyze_complete()
