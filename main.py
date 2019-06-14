from spider_random import spider_random
from spider_tag import spider_tag

MENU = '''
1)随机下载
2)指定 TAG 下载
q)退出
'''

print(MENU)
user_input = input('>>> ')
if user_input == '1':
    spider_random.run()
# elif user_input == '2':
#     spider_traverse.run()
elif user_input == '2':
    spider_tag.run()
print('程序退出')
