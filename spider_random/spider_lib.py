"""
爬虫工具函数
"""

import time

import requests


def download_img(img_save_path, img_url):
    """
    下载指定URL的图片
    :param img_save_path: 图片保存路径
    :param img_url: 图片的 URL
    :return: 下载成功返回 True，否则返回 False
    """
    # os.system('aria2c ' + img_url)
    try:
        log_print('图片下载中，国外网站下载速度较慢，如果下载超时会自动放弃，请耐心等待 ...')
        img_res = requests.get(img_url, timeout=5)
        with open(img_save_path, 'wb') as img_f:
            img_f.write(img_res.content)
        log_print(img_save_path + '√ 下载完成')
        return True
    except requests.exceptions.ConnectionError as e:
        log_print(e)
        log_print('!! 网络错误，此图片放弃 !!')
        return False
    except requests.exceptions.ReadTimeout as e:
        log_print(e)
        log_print('!! 网络错误，此图片放弃 !!')
        return False


def log_print(log):
    local_time = time.localtime()
    time_str = '[%s/%s/%s %s:%s:%s] ' % (
        local_time.tm_year, local_time.tm_mon, local_time.tm_mday,
        local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
    print(time_str, end='')
    print(log)
