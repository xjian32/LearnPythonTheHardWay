#coding=utf-8

import requests
from bs4 import BeautifulSoup
import os

#浏览器请求头
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url, headers = headers)  #使用requests的get方法，获取all_url的内容

#print(start_html.text)

#使用BeautifulSoup解析获取到的网页
Soup = BeautifulSoup(start_html.text, 'lxml')

'''
li_list = Soup.find_all('li') #find_all找到网页中li标签，返回一个列表
for li in li_list:
	print(li)
'''

a_all = Soup.find('div', class_ = 'all').find_all('a')  #先找class为all的div标签，找到后在查找所以<a>标签
for a in a_all:
	#print(a)
	title = a.get_text()  #取出a标签的文本
	href = a['href']      #取出a标签的href属性
	html = requests.get(href, headers = headers)
	html_Soup = BeautifulSoup(html.text, 'lxml')
	#查找所有<span>标签,获取第十个标签中的文本，也就是最后一个页面
	max_span = html_Soup.find('div', class_ = 'pagenavi').find_all('span')[-2].get_text()
	
	for page in range(1, int(max_span)+1):
		page_url = href + '/' + str(page)
		#print(page_url)

		#获取图片
		img_html = requests.get(page_url, headers = headers)
		img_Soup = BeautifulSoup(img_html.text, 'lxml')
		img_url = img_Soup.find('div', class_='main-image').find('img')['src']
		
		#print(img_url)

		name = img_url[-9:-4]  #去URL倒数第四位至第九位作为图片的名字
		img = requests.get(img_url, headers = headers)

		f = open(name + '.jpg', 'ab')  #多媒体文件必须用 b 参数
		f.write(img.content)           #多媒体文件用content
		f.close()
