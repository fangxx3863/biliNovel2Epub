#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def getContent(url):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	driver = webdriver.Chrome(options=options)
	
	driver.get(url)
	
	title = driver.find_element(By.ID, 'atitle')
	#print(title.text)
	
	# 获取元素的内部HTML
	inner_html = driver.find_element(By.ID, 'acontent').get_attribute('innerHTML')
	
	# 使用BeautifulSoup解析HTML
	soup = BeautifulSoup(inner_html, "html.parser")
	
	# 移除无效内容	
	for div in soup.find_all("div"):
		div.extract()
		
	# 获取处理后的HTML
	processed_html = str(soup)
	
	# 打印结果
	return processed_html
	
	# 关闭浏览器
	driver.quit()