from spider_random import spider_random
from spider_tag import spider_tag
from spider_traverse import spider_traverse

MENU = '''
1)随机下载
2)遍历图片编号下载
3)指定 TAG 下载
q)退出
'''

user_input = input(MENU)
if user_input == '1':
    spider_random.run()
elif user_input == '2':
    spider_traverse.run()
elif user_input == '3':
    spider_tag.run()
print('程序退出')
