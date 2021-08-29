import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("F:\JUPYTER NOTEBOOK\chromedriver.exe")
driver.get('https://appportal/login/')

username =  driver.find_element_by_xpath('//*[@id="loginform"]/div/div/div/input[1]')
username.send_keys = '810202558'
password = driver.find_element_by_xpath('//*[@id="loginform"]/div/div/div/input[2]')
password.send_keys ='Sgwi234!'
driver.send_keys(Keys.Enter)