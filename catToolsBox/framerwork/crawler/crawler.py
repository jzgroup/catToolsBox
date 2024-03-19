#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2023/7/6 9:32 AM
# @Author  : LTH
# @File    : crawler.py

import ssl
import urllib.request

# 插件需要的库
from bs4 import BeautifulSoup

from framerwork.log.log import Log


class Crawler:

    # 读取网址
    def getHtml(self, url):
        # 忽略证书验证错误
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        Log().info("正在读取网页：" + url)
        page = urllib.request.urlopen(url, context=ssl_context)
        html = page.read()
        # 将二进制字符串转换为文本
        html = html.decode('utf-8')
        # 断开连接
        page.close()
        return html

    # 获得腾讯文档中的表格
    def getTencentHtmlTabData(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tr_tags = soup.find_all('tr')
        table_data = []

        for tr in tr_tags:
            td_tags = tr.find_all('td')
            row_data = []
            for td in td_tags:
                if td.text:
                    row_data.append(td.text)
                else:
                    if len(row_data) > 0:
                        table_data.append(row_data)
                    break

        return table_data

    # 获得网页中的表格
    def getHtmlTabData(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tr_tags = soup.find_all('tr')
        table_data = []
        for tr in tr_tags:
            td_tags = tr.find_all('td')
            row_data = []

            for td in td_tags:
                if td.find('span'):
                    span = td.find('span')
                    row_data.append(span.text)
                elif td.find('pre'):
                    pre = td.find('pre')
                    row_data.append(pre.text)
                elif td.find('p'):
                    p = td.find('p')
                    row_data.append(p.text)

            if row_data:
                table_data.append(row_data)

        return table_data
