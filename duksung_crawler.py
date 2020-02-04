import urllib.request            # 웹브라우저에서 html문서를 얻어오기 위한 모듈
from bs4 import BeautifulSoup    # html문서 검색 모듈
import os
from selenium import webdriver   # 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
from selenium.webdriver.common.keys import Keys
import time

filename = '학사공지'

chrome = 'c:\\data\\chromedriver.exe'
browser = webdriver.Chrome(chrome)  # 웹브라우저 인스턴스화

browser.get('https://www.duksung.ac.kr/bbs/board.do?bsIdx=35&menuId=1058')

time.sleep(1)


def get_save_path():
    save_path = 'C:\\data\\덕성여대공지사항\\{}.txt'.format(filename)    # 4

    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])           # 지정된 경로에 파일이 없으면 만들어라
    return save_path


def fetch_list_url():
    params = []

    # for cnt in range(1, 5):

    browser.find_element_by_xpath("//body")       # 페이지 활성화
    html = browser.page_source                    # 현재 페이지 소스 담기 즉 1페이지
    soup = BeautifulSoup(html, "lxml")
    for i in soup.find_all('div', class_='table-responsive'):
        params.append('http://www.duksung.ac.kr' + i('a')[0]['href'])          # find_all은 리스트로 담아준다. 그래서[0]이 필요

    list_url = 'http://www.duksung.ac.kr' + soup.find_all('div', class_='table-responsive')[0]('a')[0]['href']
    #print('\n', list_url)

    for i in range(9):

        list_url = 'http://www.duksung.ac.kr' + soup.find_all('div', class_='table-responsive')[0]('a')[i]['href']

        print('\n', list_url)
        url = urllib.request.Request(list_url)
        res = urllib.request.urlopen(url).read().decode('utf-8')

        soup2 = BeautifulSoup(res, 'html.parser')     # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정

        for i in soup2.find_all('td', class_='text-left'):
            params.append('http://www.duksung.ac.kr' + i('a')[0]['href'])
    print(params)   # 페이지 내의 뉴스 웹주소 다 담긴다.
    browser.quit()
    return params

def fetch_list_url2():
    params2 = fetch_list_url()
    f = open(get_save_path(), 'w', encoding='utf-8')    # get_save_path()를 인스턴스화!!

    for i in params2:
        list_url = "{}".format(i)

        url = urllib.request.Request(list_url)
        res = urllib.request.urlopen(url).read().decode('utf-8')

        soup = BeautifulSoup(res, "html.parser")  # res html문서를 BeautifulSoup모듈을 사용해서 검색하도록 설정
        article1 = soup('div', class_= 'panel-title view-title h5')[0].get_text(strip=True, separator='\n')
        article2 = soup('div', class_='bbs_memo')[0].get_text(strip=True, separator='\n')
        # loop돌면서 기사가 계속 바뀐다.
        f.write(article1 + article2 + '\n'*2 + '='.ljust(50, '=') + '\n')  # 기사 바뀌면서 계속 적어라!

    f.close()

fetch_list_url2()
