#coding=utf-8

import requests
from bs4 import BeautifulSoup
import os

class mzitu():

	def all_url(self, url):
		html = self.request(url)        #调用requests函数把套图地址传进去，返回一个response
		all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
		for a in all_a:
			title = a.get_text()
			print(u'开始保存:', title)
			path = str(title).replace("?",'_')    #标题带有？  不能创建文件夹，需要替换
			self.mkdir(path)                      #调用mkdir函数，创建文件夹
			href = a['href']                      #取出a标签的href属性
			self.html(href)                       #调用html函数，传递href参数

	#处理套图地址，获得图片的页面地址
	def html(self, href):
		html = self.request(href)
		#查找所有<span>标签,获取第十个标签中的文本，也就是最后一个页面
		max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()

		for page in range(1, int(max_span) + 1):
			page_url = href + '/' + str(page)
			self.img(page_url)         #调用img函数


	#处理图片页面地址，获得图片的实际地址
	def img(self, page_url):
		img_html = self.request(page_url)
		img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
		self.save(img_url)


	#保存图片\
	def save(self, img_url):
		name = img_url[-9:-4]          #截取图片地址的-4位到-9位作为名字
		img = self.request(img_url)
		f = open(name + '.jpg', 'ab')
		f.write(img.content)
		f.close()


	#创建文件夹
	def mkdir(self, path):
		path = path.strip()            #移除字符串头尾指定的字符（默认为空格）
		isExists = os.path.exists(os.path.join("D:\mzitu", path))

		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件夹')
			os.makedirs(os.path.join("D:\mzitu", path))
			os.chdir(os.path.join("D:\mzitu", path))     #切换到目录
			return True
		else:
			print(u'名字叫做', path, u'的文件夹已经存在了！')
			return False


	#获取网页的response并返回
	def request(self, url):
		headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
		content = requests.get(url, headers = headers)
		return content


if __name__ == '__main__':
	Mzitu = mzitu()
	Mzitu.all_url('http://......')
