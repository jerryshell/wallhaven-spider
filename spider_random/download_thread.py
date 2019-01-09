import threading

from spider_random.spider_lib import download_img
from spider_random.spider_lib import log_print


class DownloadThread(threading.Thread):
    '''下载线程

    属性：
        thread_name: 线程名字，用于区分
        download_manager: 下载管理器
        task: 下载任务
    '''

    def __init__(self, thread_name, download_manager, task):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.download_manager = download_manager
        self.task = task
        log_print('%s 初始化完成' % self.thread_name)

    def start_download(self):
        '''开始下载

        :return: None
        '''
        log_print('%s 开始线程 URL: %s' % (self.thread_name, self.task.url))
        download_img(self.task.name, self.task.url)
        log_print('%s 线程结束 %s' % (self.thread_name, self.task.name))
        log_print('<<<<')
        self.download_manager.task_complete()

    def run(self):
        ''' 线程入口

        :return: None
        '''
        self.start_download()
