from spider_random.download_manager import DownloadManager
from spider_random.spider_lib import log_print
from spider_random.spiderwallhaven import SpiderWallhaven


class DownloadTaskCenter:
    """
    下载任务中心

    属性：
        download_manager: 下载管理器
        page_analyze_spider: 页面分析爬虫
        task_target_count: 任务目标数量
        task_list: 任务列表
        task_count: 任务计数
    """

    def __init__(self, home_page_url, download_thread_count, task_target_count):
        self.download_manager = DownloadManager(download_thread_count, self)
        self.page_analyze_spider = SpiderWallhaven(home_page_url, self)
        self.task_target_count = task_target_count
        self.task_list = []
        self.task_count = 0

    def add_task(self, task_url):
        """
        添加任务
        :param task_url: 下载任务的 URL
        :return: None
        """
        self.task_list.append(task_url)

    def get_task(self):
        """
        取得任务
        :return: 如果 task_list 不为空，返回一个 URL，否则返回 None
        """
        if len(self.task_list) > 0:
            self.task_count += 1
            log_print('>>>> 第 %s 号任务开始执行' % self.task_count)
            return self.task_list.pop(0)
        else:
            return None

    def drive_page_analyze(self):
        """
        驱动页面分析
        :return: None
        """
        log_print('========== 页面分析阶段开始 ==========>>')
        if self.task_count < self.task_target_count:
            self.page_analyze_spider.run()
        else:
            log_print('任务完成')
        log_print('========== 页面分析阶段结束 ==========<<')

    def drive_downloader(self):
        """
        驱动下载器
        :return: None
        """
        log_print('---------- 下载任务阶段开始 ---------->>')
        self.download_manager.start_download_task()
        log_print('线程初始化完毕')
