#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 20:31
# @Author  : flyhawk
# @Site    : 
# @File    : bilibili_rename_and_move.py
# @Software: PyCharm

import os
from Crawl import Crawler
from lxml import etree


class BilibiliRenameAndMove(Crawler):

	def __init__(self, target_url='', target_path='', deal_method='2'):
		Crawler.__init__(self)
		self.bilibili_url = target_url
		self.target_path = target_path
		self.xpath_rule = '/html/body/div[3]/div/div[2]/div[3]/div[2]/ul/li/*'
		self.deal_method = deal_method
		self.episode_list_dic = {}
		self.serials_number_length = 0

	def get_episode_list(self):
		# html = self.get_html(self.bilibili_url)
		if os.path.exists(os.path.join(self.target_path, 'bilibili.htm')):
			html = self.get_local_html(os.path.join(self.target_path, 'bilibili.htm'))
		elif os.path.exists(os.path.join(self.target_path, 'bilibili.html')):
			html = self.get_local_html(os.path.join(self.target_path, 'bilibili.html'))
		else:
			raise RuntimeError('file do not exist!!')

		list = self.get_list(html, self.xpath_rule)
		self.serials_number_length = len(str(len(list)))
		for _list in list:
			# /html/body/div[3]/div/div[2]/div[3]/div[2]/ul/li[1]/a/span
			num = _list.xpath("./span")
			print(num[0].text)
			print(num[0].tail)
			# zfill函数用来给字符串前面补0
			episode_number = num[0].text.strip('P').zfill(self.serials_number_length)
			episod_name = num[0].tail.strip()
			self.episode_list_dic[episode_number] = episod_name

	def rename_and_move_episode(self, episode_folder, _path):
		list = os.listdir(_path)  # 列出文件夹下所有的目录与文件
		for i in range(0, len(list)):
			filepath = os.path.join(_path, list[i])
			if os.path.isdir(filepath):
				self.rename_and_move_episode(episode_folder, filepath)
			if os.path.isfile(filepath):
				file_path, file_name_ext = os.path.split(filepath)
				file_name, file_ext = os.path.splitext(file_name_ext)
				target_filepath = ''
				if file_ext == '.blv':
					episode_number = episode_folder.zfill(self.serials_number_length)
					if self.deal_method == '1':
						target_filepath = os.path.join(self.target_path, self.episode_list_dic[episode_number]
						                               + '.' + file_name + ".flv")
					else:
						target_filepath = os.path.join(self.target_path,
						                               episode_number+ '-' + self.episode_list_dic[episode_number]
						                               + '.' + file_name + ".flv")

					os.rename(filepath, target_filepath)

				elif file_ext == '.m4s':
					episode_number = episode_folder.zfill(self.serials_number_length)
					if file_name == 'audio':
						target_filepath = os.path.join(self.target_path, self.episode_list_dic[episode_number]
													   + '.' + file_name + ".mp3")
					if file_name == 'video':
						target_filepath = os.path.join(self.target_path, self.episode_list_dic[episode_number]
													   + '.' + file_name + ".mp4")

					os.rename(filepath, target_filepath)

	def do_job(self):
		self.get_episode_list()
		list = os.listdir(self.target_path)  # 列出文件夹下所有的目录与文件
		for episode_folder in list:
			episode_path = os.path.join(self.target_path, episode_folder)
			if os.path.isdir(episode_path):
				self.rename_and_move_episode(episode_folder, episode_path)


def main():
	target_url = '' # input("请输入视频URL: ")
	tartet_path = input("请输入存放视频的目录，并将要处理的网页另存为“bilibili.htm”该目录: ")
	deal_method = input("1、清除原序号；2、补足原序号: ")

	# target_url = "https://www.bilibili.com/video/av8475172"
	# tartet_path = 'G:\8475172'
	# deal_method = '2'

	job = BilibiliRenameAndMove(target_url, tartet_path, deal_method)
	job.do_job()

	# "https://www.bilibili.com/video/av24817093"
	# /html/body/div[3]/div/div[2]/div[3]/div[2]/ul/li[1]/a


if __name__ == '__main__':
	main()

