from spider_random.download_task_center import DownloadTaskCenter


def run():
    home_page_url = 'https://alpha.wallhaven.cc/random'
    try:
        get_home_page_count = int(input('请求 1 次首页可获得 24 张图片，你要请求多少次（默认：1）\n>>> '))
        if get_home_page_count < 1:
            raise ValueError
    except ValueError:
        get_home_page_count = 1

    try:
        thread_count = int(input('你要开启多少个下载线程？（默认：4）\n>>> '))
        if thread_count < 1:
            raise ValueError
    except ValueError:
        thread_count = 4

    task_center = DownloadTaskCenter(home_page_url, thread_count, get_home_page_count * 24)
    task_center.drive_page_analyze()
