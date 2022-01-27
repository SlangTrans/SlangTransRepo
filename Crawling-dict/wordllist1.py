import re
import time
import csv
import json
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
driver.get('https://open.dict.naver.com/participation/word_list.dict#common/register_user/ko/ko/u1436cd4f6448f3d9891353dfc514acb66')
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
wordlist1= []
for item in words:
    temp = []
    
    try:
        words = item.select_one("#wordRegisterList > li > p.usen_entry > span.word_wrap > a").text
        meaning = item.select_one("#wordRegisterList > li > p.usen_mean > a").text
        words= words.replace("\n","")
        meaning = meaning.replace("\n","")
        words= words.replace("\t","")
        meaning = meaning.replace("\t","")
        temp.append(words)#wordRegisterList > li:nth-child(3) > p.usen_entry > span.word_wrap > a
        temp.append(meaning)
    except Exception as e:
        continue
        
    
    wordlist1.append(temp)
# print(wordlist)
with open('wordlist1.csv',"w",encoding ="utf-8-sig", newline ="") as f:
    writer = csv.writer(f)
    writer.writerow(['단어','의미'])
    writer.writerows(wordlist1)

f.close
with open('wordlist1.json', 'w', encoding='utf-8') as file :
        json.dump(wordlist1, file, ensure_ascii=False, indent='\t')


file.close
    
# for i in range(5):
#     print(wordllist[i])
# html = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[4]/div[2]/ul')
# print(html.text)
# html = driver.find_element_by_xpath('//*[@id="wordRegisterList"]')
# print(html.text)