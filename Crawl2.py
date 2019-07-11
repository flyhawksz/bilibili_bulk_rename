#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/16 21:46
# @Author  : flyhawk
# @Site    :
# @File    : CralProxyAndVerfiy.py
# @Software: PyCharm


"""
爬虫父类，放置通用的方法
"""


import requests
from lxml import etree
import logging  # log相关功能，不能总是用print那么low
import socket  # 用于设定网络连接的相关属性
import codecs
from abc import ABCMeta, abstractmethod


class Crawler(metaclass=ABCMeta):
    crawl_target = ''

    @abstractmethod
    def get_html(self):
        pass

    def set_target(self, target):
        self.crawl_target = target

        # 解析网页，并得到网页中的ID,保存为文件

    def get_list(self, html, xpath_rule):
        gain_list = []
        # 对获取的页面进行解析
        selector = etree.HTML(html)
        gain_list = selector.xpath(xpath_rule)
        # 计算每个页面一共有几个IP地址
        print('gain %d records' % len(gain_list))
        logging.info('Get list %d' % len(gain_list))
        return gain_list

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def get_item(self):
        pass


class WebCrawler(Crawler):

    def __init__(self):  # 类的初始化函数，在类中的函数都有个self参数，其实可以理解为这个类的对象
        # 要为http报文分配header字段，否则很多页面无法获取
        self.http_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept-Encoding': 'gzip, deflate'
        }

        # 配置log信息存储的位置
        logging.basicConfig(filename='./debug.log', filemode="w", level=logging.DEBUG)
        # 3秒内没有打开web页面，就放弃等待，防止死等，不管哪种语言，都要防范网络阻塞造成程序响应迟滞，CPU经常因此被冤枉
        socket.setdefaulttimeout(3)

    # 返回网页代码
    def get_html(self,):
        response = requests.get(self.crawl_target, headers=self.http_headers)
        response.encoding = 'utf-8'
        # print(response.text)
        return response.text


class LocalCrawler(Crawler)
    # 返回本地文件
    def get_local_html(self, filepath):
        f = codecs.open(filepath, 'r', 'utf-8')
        html = f.read()
        f.close()
        return html

    # 代理IP的信息存储
    def write_list_txtfile(self, list, filename):
        # print(proxies)
        for t_list in list:
            # with as 语法的使用，可以省去close文件的过程
            with open(filename, 'a+', encoding="UTF-8") as f:
                logging.info("Writing ：%s" % t_list)
                f.write(t_list + '\n')
        logging.info("Finish Writing!!!")

    def write_queue_txtfile(self, queue, filename):
        # print(proxies)
        while not queue.empty():
            t_queue = queue.get()
            # with as 语法的使用，可以省去close文件的过程
            with open(filename, 'a+', encoding="UTF-8") as f:
                logging.info("Writing ：%s" % t_queue)
                f.write(t_queue)
        logging.info("Finish Writing!!!")
