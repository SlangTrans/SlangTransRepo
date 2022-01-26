import re
import time
import csv
# print(html.decode("utf-8"))
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')   
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

driver.implicitly_wait(10)
driver.get('https://nid.naver.com/nidlogin.login')
driver.find_element_by_name('id').send_keys('youtID')
driver.find_element_by_name('pw').send_keys('yourPSW')
driver.find_element_by_xpath('//*[@id="log.login"]').click()
# header = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
driver.get('https://open.dict.naver.com/participation/word_list.dict#common/register_user/ko/ko/u1436cd4f6448f3d9891353dfc514acb66')
# driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[4]/div[1]/div[2]/div[2]/button[2]/span').click()
html = driver.find_element_by_xpath('//*[@id="wordRegisterList"]')
print(html.text)
loop, count = True, 0
while loop and count < 35:
    try:
        driver.find_element_by_xpath('//*[@id="moreview"]/div/button').click()
        count = count + 1
        time.sleep(1)
    except TimeoutException:
        loop = False
        
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# items = soup.select("#wordRegisterList")
words = soup.select("#wordRegisterList > li")
wordlist= []
for item in words:
    temp = []
    
    try:
        words = item.select_one("#wordRegisterList > li > p.usen_entry > span.word_wrap > a").text
        meaning = item.select_one("#wordRegisterList > li > p.usen_mean > a").text
        temp.append(words)#wordRegisterList > li:nth-child(3) > p.usen_entry > span.word_wrap > a
        temp.append(meaning)
    except Exception as e:
        continue
        
    
    wordlist.append(temp)
print(wordlist)
with open('wordlist.csv',"w",encoding ="utf-8-sig", newline ="") as f:
    writer = csv.writer(f)
    writer.writerow(['단어','의미'])
    writer.writerows(wordlist)

f.close

    
# for i in range(5):
#     print(wordllist[i])
# html = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[4]/div[2]/ul')
# print(html.text)
# html = driver.find_element_by_xpath('//*[@id="wordRegisterList"]')
# print(html.text)