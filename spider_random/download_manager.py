from spider_random.download_thread import DownloadThread
from spider_random.spider_lib import log_print


class DownloadManager:
    '''下载管理器

    属性：
        max_download_thread_count: 最大下载线程数量
        free_download_thread_count: 空闲下载线程数量
        running_download_thread_count: 运行中下载线程数量
    '''

    def __init__(self, max_download_thread_count, download_task_center):
        self.max_download_thread_count = max_download_thread_count
        self.free_download_thread_count = max_download_thread_count
        self.running_download_thread_count = 0
        self.download_task_center = download_task_center

    def start_download_task(self):
        '''开始下载任务

        :return: None
        '''
        for i in range(self.free_download_thread_count):
            self.start_new_download_thread()

    def get_task(self):
        '''从任务中心获取任务

        :return: None
        '''
        return self.download_task_center.get_task()

    def start_new_download_thread(self):
        '''开启一个新的下载线程，并且给线程分配任务

        :return: None
        '''
        if self.free_download_thread_count == 0:
            return
        task = self.get_task()
        if not task:
            if self.free_download_thread_count == self.max_download_thread_count:
                log_print('---------- 下载任务阶段结束 ----------<<')
                log_print('任务列表为空 --- 开始驱动页面分析')
                self.download_task_center.drive_page_analyze()
            return
        new_download_thread_name = '线程 ' + str(task.name)
        new_download_thread = DownloadThread(new_download_thread_name, self, task)
        new_download_thread.start()
        self.free_download_thread_count -= 1
        self.running_download_thread_count += 1

    def task_complete(self):
        '''下载线程结束时回调这个方法，开启新的下载线程

        :return: None
        '''
        self.free_download_thread_count += 1
        self.running_download_thread_count -= 1
        self.start_new_download_thread()
        log_print('运行中的线程数量：%s' % self.running_download_thread_count)
