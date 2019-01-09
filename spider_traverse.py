from multiprocessing import Pool

import requests
import requests.exceptions

# 超时时间
TIMEOUT = 10


def get_image(image_num):
    image_url_tmp = 'http://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.%s'
    try:
        # jpg 格式
        image_suffix = 'jpg'
        image_url = image_url_tmp % (image_num, image_suffix)
        print('正在下载 %s' % image_url)
        response = requests.get(image_url, timeout=TIMEOUT)
        if response.status_code == 200:
            print('%s 状态码: 200' % image_num)
        # png 格式
        elif response.status_code == 404:
            print('%s 状态码: 404' % image_num)
            image_suffix = 'png'
            image_url = image_url_tmp % (image_num, image_suffix)
            print('正在下载 %s' % image_url)
            response = requests.get(image_url, timeout=TIMEOUT)
        # 未知格式，记录错误
        else:
            with open('error.txt', 'a') as f:
                f.write('%s unknown format\n' % image_num)
                f.write('image_url: %s' % image_url)
                f.write('response.status_code: %s' % response.status_code)
                f.write('---')
        # 写入文件
        filename = 'wallhaven-%s.%s' % (image_num, image_suffix)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print('%s\tOK' % filename)
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.Timeout as e:
        print(e)
    except KeyboardInterrupt:
        print('Exit')


def run():
    max_num = 298879
    print('最大图片编号：%s' % max_num)
    try:
        start_num = int(input('请输入起始图片编号（默认：1）\n>>> '))
    except ValueError:
        start_num = 1
    try:
        processes = int(input('下载线程（默认：4）\n>>> '))
    except ValueError:
        processes = 4
    pool = Pool(processes)
    pool.imap(get_image, range(start_num, max_num + 1))
    pool.close()
    pool.join()


if __name__ == '__main__':
    run()
