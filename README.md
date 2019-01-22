# Spider Wallhaven

wallhaven.cc 爬虫

# 功能

* 随机下载
* 遍历图片编号下载
* 指定 TAG 下载

# 运行

```bash
python3 ./main.py
```

# 依赖

* requests
* bs4

# FAQ

Q: 为什么 spider_random 的代码这么复杂？

A: 因为 spider_random 实现了类似线程池的功能，我当时还不知道 multiprocessing 这个包，但是也有好处，因为 multiprocessing 不支持 Windows，而 spider_random 因为自己实现了线程池所以可以在 Windows 中正常运行。

# 推荐

[下载的图片当中有很多都是自己不喜欢的？希望以后可以针对性的下载自己喜欢的图片？这里有个项目可以根据你保留下来的 wallhaven.cc 图片找出最喜欢的标签](https://github.com/jerryshell/favorite-wallhaven-tag)
