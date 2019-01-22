"""
通过遍历图片编号来下载图片
"""
from multiprocessing import Pool

import requests
import requests.exceptions

# 超时时间
TIMEOUT = 10


def download_image(image_number):
    """
    下载图片
    :param image_number: 图片编号
    :return:
    """
    image_url_tmp = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.%s'
    try:
        # jpg 格式
        image_suffix = 'jpg'
        image_url = image_url_tmp % (image_number, image_suffix)
        print('正在下载 %s' % image_url)
        response = requests.get(image_url, timeout=TIMEOUT)
        if response.status_code == 200:
            print('%s 状态码: 200' % image_number)
        # png 格式
        elif response.status_code == 404:
            print('%s 状态码: 404' % image_number)
            image_suffix = 'png'
            image_url = image_url_tmp % (image_number, image_suffix)
            print('正在下载 %s' % image_url)
            response = requests.get(image_url, timeout=TIMEOUT)
        # 未知格式，记录错误
        else:
            with open('error.txt', 'a') as f:
                f.write('%s unknown format\n' % image_number)
                f.write('image_url: %s' % image_url)
                f.write('response.status_code: %s' % response.status_code)
                f.write('---')
        # 写入文件
        filename = 'wallhaven-%s.%s' % (image_number, image_suffix)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print('%s\tOK' % filename)
    except KeyboardInterrupt:
        print('Exit')
    except Exception as e:
        print(e)


def run():
    """
    开始运行
    :return:
    """
    max_number = 298879
    print('最大图片编号：%s' % max_number)
    try:
        start_number = int(input('请输入起始图片编号（默认：1）\n>>> '))
    except ValueError:
        start_number = 1
    try:
        processes = int(input('下载线程（默认：4）\n>>> '))
    except ValueError:
        processes = 4
    pool = Pool(processes)
    pool.imap(download_image, range(start_number, max_number + 1))
    pool.close()
    pool.join()


if __name__ == '__main__':
    run()
