from bs4 import BeautifulSoup    # html 소스를 전부 가져오는 기능
from selenium import webdriver    # 브라우저 실행 및 검색창, 버튼 조작
import time    # 페이지 열기에 필요한 시간만큼 대기하는 기능
import sys    # 파일 작성할 때 필요
import os    # 경로 설정할 때 필요
import pandas as pd
import xlwt

search_txt = ""    # 검색어. 사용자의 input에 따라 주차 혹은 정차가 대입됨.

while(True):

    num = input('<<검색어 선택>>\n  0 : 전체    1 : 주차    2 : 정차    3: 공단(테스트용) \n')

    if(num.isdecimal() == False):    # 만약 입력값이 정수가 아닐 경우 루프를 처음부터 시작
        print('잘못된 값입니다.\n')
        continue

    num = int(num)

    if(num == 0):
        search_txt = ''    # 아무것도 입력 안하고 검색하면 전체글이 나옴
        break
    elif(num == 1):
        search_txt = '주차'
        break
    elif num == 2 :
        search_txt = '정차'
        break
    elif num == 3 :
        search_txt = '공단'    # 검색결과가 14페이지라 다음 페이지 버튼도 클릭하면서
        break                  # 검색결과를 끝까지 잘 크롤링하는지 테스트하는 용도로 넣었음
    else:
        print('잘못된 값입니다.\n')

hope_page = -1

while(True):
    num = input('<<크롤링할 페이지 수>>\n  0 혹은 전체 페이지 수보다 큰 숫자를 입력할 경우\n  전체 페이지를 크롤링합니다.\n')
    
    if(num.isdecimal() == False):
        print('잘못된 값입니다.\n')
        continue
    
    num = int(num)  

    if(num < 0):
        print('잘못된 값입니다.\n')
        continue
    
    hope_page = num
    break

os.path.join(os.path.dirname(__file__))
dir_path = os.path.dirname(os.path.realpath(__file__))    # 현재 실행중인 이 파일의 위치를 dir_path에 저장


path = dir_path + "/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.changwon.go.kr/mayor/civil/voice/list.do?ptIdx=105&mId=0401000000")
time.sleep(2)    # 사이트가 열릴 때까지 대기


searchElement = driver.find_element_by_id("searchTxt")    # 현재 페이지에서 id로 검색창을 찾기
searchElement.send_keys(search_txt)    # 검색어(search_txt)를 검색창에 입력

driver.find_element_by_class_name("small").click()    # 검색 버튼을 찾아서 클릭 (클래스이름에 띄어쓰기가 있을 경우 인식을 못하므로 클래스이름의 일부로 검색 by 규동)
time.sleep(1)

full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')    # 현재 페이지 html 소스 전체를 문자로 변환하여 soup 변수에 저장



total_page = int(soup.find('p', class_ = 'page_num').get_text().replace('\n','').strip().replace(' ','').split('/')[1][5:])    # 전체 페이지 수

if(hope_page != 0 and hope_page < total_page):    # 만약 희망 페이지 수가 0이 아니고 전체 페이지 수보다 작으면
    total_page = hope_page    # 페이지수에 희망 페이지 수를 대입


page_cnt = 0

count = []    # 처음부터 끝까지 잘 됐는지 확인용 카운트
number = []    # 글번호
title = []    # 글제목
date = []    # 연월일
part = []    # 부서



while True:

    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')
    content_list = soup.find('table',class_='bod_list').find('tbody').find_all('tr')
    
    cnt = 0

    for tr in content_list:
        
        tmp_number = tr.find('td', class_ = 'list_num').get_text()    # 글번호
        tmp_title = tr.find('td', class_ = 'list_tit').get_text().replace("\n",'').strip().split(']')[1].lstrip()    # 글제목
        tmp_part = tr.find('td', class_ = 'deptNm').get_text().replace("\n",'').strip()    # 담당부서
        tmp_date = tr.find('td', class_ = 'date').get_text().replace("\n",'').strip()    # 날짜
        tmp_date = tmp_date[:10] + ' ' + tmp_date[10:]
    
        number.append(tmp_number)
        title.append(tmp_title)
        part.append(tmp_part)
        date.append(tmp_date)

        cnt += 1

        count.append(cnt + page_cnt * 10)

        try:
            print(cnt + page_cnt*10,':',tmp_number,tmp_title)
        except:
            print('UnicodeEncodeError')

    page_cnt += 1

    if(page_cnt == total_page):
        break
    else:
        div = page_cnt % 10
        if(div == 0):
            print('다음 10페이지')
            try:
                driver.find_element_by_class_name('btn_10next').click()
            except:
                driver.refresh()
                try:
                    driver.find_element_by_class_name('btn_10next').click()
                except:
                    pass
            time.sleep(0.1)

        else:
            print('페이지이동 실행:', page_cnt + 1)
            try:
                driver.find_element_by_xpath('//*[@title="%s페이지로 이동"]'%(page_cnt + 1)).click()
            except:
                driver.refresh()
                try:
                    driver.find_element_by_xpath('//*[@title="%s페이지로 이동"]'%(page_cnt + 1)).click()
                except:
                    pass
            time.sleep(0.1)



from datetime import datetime    # 파일명을 날짜시간별로 정하기 위해 사용
now = datetime.now()


all_contents = pd.DataFrame()

all_contents['카운트'] = count
all_contents['글번호'] = number
all_contents['제목'] = title
all_contents['담당부서'] = part
all_contents['날짜'] = date

if(search_txt == ''):
    search_txt = '전체'

f_path = dir_path + '/' + str(now).split('.')[0].replace(':','').replace(' ','_') + '_' + search_txt + '_' + str(total_page) + 'page' + '.xls'
all_contents.to_excel(f_path)


print('\n모든 작업이 끝났습니다.')