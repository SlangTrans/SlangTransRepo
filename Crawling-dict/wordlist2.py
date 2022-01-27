# import urllib.request as url

# response = url.urlopen("https://open-pro.dict.naver.com/_ivo/dictmain?dictID=enegdwdxdyebegdxdwdsqyofehjosqff/html/body/div[1]/div/div/div/div[2]/div[2]/div[4]/div[2]/ul/div[1]/a/strong/span[1]")

# html = response.read()
import re
# print(html.decode("utf-8"))
from selenium import webdriver
import time
import csv
import json
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')   
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe')

driver.implicitly_wait(10)
driver.get('https://nid.naver.com/nidlogin.login')

header = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
driver.get('https://open-pro.dict.naver.com/_ivo/dictmain?dictID=enegdwdxdyebegdxdwdsqyofehjosqff&orderType=update_time&listType=1')
wordlist2= []
loop, count = True,0
while loop and count < 5:
    try:
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[4]/div[3]/button['+str(count+1)+']').click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        words = soup.select("#content > div.section-main > div.word > div.result > ul > div")
        
        for item in words:
            temp = []
    
            try:
                words = item.select_one("#content > div.section-main > div.word > div.result > ul > div > a > strong > span:nth-child(1)").text
                meaning = item.select_one("#content > div.section-main > div.word > div.result > ul > div > a > div.card-desc > span").text
                
                words= words.replace("\n","")
                meaning = meaning.replace("\n","")
                
                temp.append(words)#wordRegisterList > li:nth-child(3) > p.usen_entry > span.word_wrap > a
                temp.append(meaning)
            except Exception as e:
                continue
        
    
            wordlist2.append(temp)
        
        count = count + 1
        time.sleep(1)
    except TimeoutException:
        loop = False
with open('wordlist2.csv',"w",encoding ="utf-8-sig", newline ="") as f:
    writer = csv.writer(f)
    writer.writerow(['단어','의미'])
    writer.writerows(wordlist2)

f.close

with open('wordlist2.json', 'w', encoding='utf-8') as file :
        json.dump(wordlist2, file, ensure_ascii=False, indent='\t')


file.close