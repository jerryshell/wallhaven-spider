"""
通过指定 TAG 下载图片
"""
from multiprocessing import Pool

import requests
import requests.exceptions
from bs4 import BeautifulSoup

# 超时时间
TIMEOUT = 10


def get_max_page(tag):
    """
    获取最大页数
    :param tag: 标签
    :return: max_page
    """
    tag_url_tmp = 'https://wallhaven.cc/search?q={0}'
    home_page_url = tag_url_tmp.format(tag)
    response = requests.get(home_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_elem = soup.select_one('#main > header > h1')
    if title_elem is None:
        print('这个标签可能不存在 {0}'.format(home_page_url))
        return -1
    return int(title_elem.text.split(' ')[0].replace(',', ''))


def analysis_tag_home_page(tag, page):
    """
    分析标签主页
    :param tag: 标签
    :param page: 页数
    :return: image_detail_urls
    """
    tag_url_tmp = 'https://wallhaven.cc/search?q={0}&page={1}'
    home_page_url = tag_url_tmp.format(tag, page)
    image_detail_urls = []

    try:
        response = requests.get(home_page_url, timeout=TIMEOUT)
        soup = BeautifulSoup(response.text, 'html.parser')

        image_a_tags = soup.find_all('a', class_='preview')
        image_detail_urls = []
        for image_a_tag in image_a_tags:
            image_detail_urls.append(image_a_tag['href'])

    except requests.exceptions.ReadTimeout as e:
        print(e)
    finally:
        return image_detail_urls


def analysis_image_detail_page(image_detail_urls):
    """
    分析页面详情页
    :param image_detail_urls: 页面详情页列表
    :return: image_urls
    """
    image_urls = []
    try:
        for image_detail_url in image_detail_urls:
            response = requests.get(image_detail_url, timeout=TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')

            img_tag = soup.find('img', id='wallpaper')
            image_url = img_tag['src']
            print('image_urls.append {0}'.format(image_url))
            image_urls.append(image_url)

    except requests.exceptions.ReadTimeout as e:
        print(e)
        print('连接超时')
    finally:
        return image_urls


def download_image(image_url: str):
    """
    下载图片
    :param image_url: 图片 URL
    """
    try:
        response = requests.get(image_url, timeout=TIMEOUT)
        # image_name = re.findall(r'wallhaven-\d+.*', image_url)[0]
        image_name = image_url.split('/')[-1]

        with open(image_name, 'wb') as f:
            f.write(response.content)
        print('{0} 下载完成'.format(image_name))

    except requests.exceptions.ReadTimeout as e:
        print(e)
        print('连接超时')


def downloader(processes, image_urls):
    """
    多线程下载器
    :param processes: 线程数量
    :param image_urls: 图片 URL 列表
    """
    pool = Pool(processes)
    pool.imap(download_image, image_urls)
    pool.close()
    pool.join()


def run():
    """
    爬虫入口
    """
    target_tag = input('请输入要采集的标签（默认：artwork）\n>>> ')
    if target_tag == '':
        target_tag = 'artwork'

    print('开始获取最大页数 ...')
    max_page = get_max_page(target_tag)
    print('最大页数 = {0}'.format(max_page))

    try:
        page_start = int(input('请输入起始页数（默认：1）\n>>> '))
        if page_start < 1:
            raise ValueError
    except ValueError:
        page_start = 1

    try:
        page_end = int(input('请输入终止页数（默认：最大页数）\n>>> '))
        if page_end > max_page:
            raise ValueError
    except ValueError:
        page_end = max_page

    try:
        download_processes = int(input('下载线程（默认：4）\n>>> '))
        if download_processes < 1:
            raise ValueError
    except ValueError:
        download_processes = 4

    for page in range(page_start, page_end + 1):
        print('开始分析标签主页 ...')
        image_detail_urls = analysis_tag_home_page(target_tag, page)

        print('开始分析图片详情页 ...')
        image_urls = analysis_image_detail_page(image_detail_urls)

        print('开始下载 ...')
        downloader(download_processes, image_urls)


if __name__ == '__main__':
    run()
