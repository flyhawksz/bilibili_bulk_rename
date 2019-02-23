#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/23 16:32
# @Author  : flyhawk
# @Site    : 
# @File    : bulk_rename.py
# @Software: PyCharm
import os


file_path = 'G:\\temp\\宏观经济学-复旦'


def main(_path):
	list = os.listdir(_path)  # 列出文件夹下所有的目录与文件
	for i in range(0, len(list)):
		filepath = os.path.join(_path, list[i])
		if os.path.isdir(filepath):
			pass
		if os.path.isfile(filepath):
			file_path, file_name_ext = os.path.split(filepath)
			file_name, file_ext = os.path.splitext(file_name_ext)
			if file_ext == '.flv':
				new_filepath = os.path.join(_path,file_name_ext.split("讲-")[1])
				os.rename(filepath, new_filepath)


if __name__ == '__main__':
	main(file_path)