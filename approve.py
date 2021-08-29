import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path="F:\JUPYTER NOTEBOOK\chromedriver.exe")
driver.get('https://approweb.intranet.pajak.go.id/')

driver.find_element_by_xpath('//*[@id="LoginForm_ip"]').send_keys('958630731')
driver.find_element_by_xpath('//*[@id="LoginForm_kataSandi"]').send_keys('LaTahzan7')
driver.find_element_by_xpath('//*[@id="yw0"]/div[5]/button').click()
alert = driver.switch_to.alert()
alert.dismiss()

