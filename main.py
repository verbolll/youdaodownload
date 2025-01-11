from pdfmethod import split_pdf, get_num_pages
from pdfmethod import AppendPdf
from selenium import webdriver
from selenium.webdriver.common.by import By
from browsermobproxy import Server
import urllib.request
import shutil
import os
import json


server = Server(r".\browsermob-proxy\bin\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
chrome_options.add_argument('ignore-certificate-errors')

path = os.getcwd()

# 替换要翻译的文件
Name = 'Assessment of the methodology for the CFD simulation of the flight of a quadcopter UAV'
pdfName = Name + '.pdf'
pages = get_num_pages(pdfName) + 1
split_pdf(pdfName, 1)

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window()
proxy.new_har("my_har")

# 下载
for i in range(1,pages):
    browser.implicitly_wait(100)
    url = 'https://fanyi.youdao.com/#/documentUpload'
    xpath = '//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div[2]/div/input'
    browser.get(url)
    file_input = browser.find_element(By.XPATH, xpath)
    file_input.send_keys(rf"{path}\{Name}\{i}.pdf" )
    xpath = '//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div[1]'
    lang = browser.find_element(By.XPATH, xpath)
    lang.click()
    xpath = '//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div/div/table/tr[1]/td[2]/div/div'
    enzh = browser.find_element(By.XPATH, xpath)
    enzh.click()
    xpath = '//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/div/div/div/div[3]/div[2]/div'
    tran = browser.find_element(By.XPATH, xpath)
    while 1:
        try:
            tran.click()
            break
        except:
            pass
    while 1:
        try:
            xpath = '//*[@id="doctrans-web"]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div/div/div'
            browser.find_element(By.XPATH, xpath)
            break
        except:
            pass
browser.quit()

har_data = proxy.har
with open('hex.json', 'w') as fp:
    fp.write('[\n')
    for entry in har_data['log']['entries']:
        fp.write(json.dumps(entry, indent=2))
        fp.write(',\n')

# 规范json文件格式
with open('hex.json', 'r') as fp:
    lines = fp.readlines()
    lines = lines[:-1]
with open('hex.json', 'w', encoding='utf-8') as fp:
    fp.writelines(lines)
    fp.write('}\n]')

# 逐页下载pdf
with open('hex.json', 'r') as fp:
    data = json.load(fp)
    urls = [entry['request']['url'] for entry in data if 'getFirst' in entry['request']['url']]
    print(*(i for i in urls), sep='\n')
for url, i in zip(urls, range(1,pages)):
    while 1:
        try:
            j = str(i).zfill(5)
            urllib.request.urlretrieve(url, f"./pdf/{j}.pdf")
            break
        except:
            pass

# 合并pdf
mergeePdfList = ['./pdf/' + i for i in os.listdir('./pdf/')]
appendpdf = AppendPdf(mergeePdfList, Name)
appendpdf.merger_pdf()
appendpdf.returnPdf()

for i in ['./pdf/' + i for i in os.listdir('./pdf/')]:
    os.remove(i)
shutil.rmtree(Name)
os.popen('Zh' + Name + '.pdf')