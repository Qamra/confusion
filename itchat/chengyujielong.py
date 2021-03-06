#!/usr/local/python/bin/python
# coding=utf-8
from urllib import parse, request
from bs4 import BeautifulSoup
import random
from pypinyin import lazy_pinyin
import Pinyin2Hanzi
from Pinyin2Hanzi import DefaultDagParams, dag
from itertools import chain


def get_chengyu(word):
	bigger_list = []
	if Pinyin2Hanzi.is_chinese(word):
		word_pinyin = lazy_pinyin(word)
		dagParams = DefaultDagParams()
		word_list = []
		result = dag(dagParams, word_pinyin, path_num=3, log=True)
		for item in result:
			word_list.append(item.path[0])
		# print(word_list)
		for avg_word in word_list:
			if find_chengyu(avg_word) != "Null":
				bigger_list.append(find_chengyu(avg_word))

		heiheihei = list((chain(*bigger_list)))
		# print(heiheihei)
		max_len = len(heiheihei) - 1
		flag = random.randint(0, max_len)
		return heiheihei[flag]
	else:
		return 1


def find_chengyu(end_str):
	temp_list = []
	end_str = end_str.encode('gb2312')
	header = {'Useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
	          'Connection': 'keep-alive',
	          'Host': 'cy.5156edu.com'}
	base_url = 'http://cy.5156edu.com/serach.php'
	post_args = {'f_key': end_str, 'f_type': 'chengyu', 'f_type2': '1'}
	post_args = parse.urlencode(post_args).encode('gb2312')
	req = request.Request(base_url, headers=header, data=post_args)
	html = request.urlopen(req).read()
	soup = BeautifulSoup(html, 'html.parser', from_encoding="gb18030")
	big_list = soup.table.contents[1].contents[1].contents[1].contents[11].contents[2:]
	[big_list.remove(i) for i in big_list if i == '\n']
	for j in big_list:
		temp_list.append(str(j).split('u', 1)[1].split('>')[1].split('<')[0].strip())
	fin_list = temp_list[:]
	for k in temp_list:
		if k[0].encode('gb2312') != end_str:
			fin_list.remove(k)
	# print(fin_list)
	if len(fin_list) == 0:
		return "Null"
	else:
		return fin_list


if __name__ == '__main__':
	# print(find_chengyu("哈"))
	print(get_chengyu("像"))
