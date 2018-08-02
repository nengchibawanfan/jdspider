from selenium import webdriver
from lxml import etree


driver = webdriver.Chrome()
driver.get('http://www.baidu.com')
html = etree.HTML(driver.page_source)
print(html.xpath('/html/head/title/@text()'))
driver.close()