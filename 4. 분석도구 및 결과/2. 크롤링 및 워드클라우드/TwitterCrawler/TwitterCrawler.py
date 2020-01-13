from bs4 import BeautifulSoup    # html 소스를 전부 가져오는 기능
from selenium import webdriver    # 브라우저 실행 및 검색창, 버튼 조작
import time    # 페이지 열기에 필요한 시간만큼 대기하는 기능
import sys    # 파일 작성할 때 필요
import os    # 경로 설정할 때 필요
from datetime import datetime, timedelta    # 파일명을 날짜시간별로 정하기 위해 사용
import calendar    # 시차변경 날짜계산에 필요
import pandas as pd    # 데이터프레임 작성에 필요
import xlwt    # 엑셀파일로 저장에 필요


print('=' * 80)
print('  창원교통정보센터 트위터 웹크롤러입니다.')
print('  원하는 기간(연월)을 입력하면 한 달 간격으로 엑셀파일을 생성합니다.')
print('  만약 작업 도중 프로그램이 예기치 않게 종료된다면')
print('  이전 작업에 이어서 작업을 실행합니다.')
print('=' * 80)
print('\n')

while(True):
    dateInput = input('<<크롤링할 연도>>\n  2015~2019 범위에서 크롤링할 연도를 입력해주세요.\n  (예시: 2017)\n')
    
    if(dateInput.isdecimal() == False):
        print('다시 입력해주세요.\n')
        continue
    
    if(int(dateInput) < 2015 or int(dateInput) > 2019):
        print('다시 입력해주세요.\n')
        continue

    dateRange = []
    for oneMonth in range(1,13):
        
        if(dateInput == '2019' and datetime.now().month + 1 == oneMonth):
            break

        mon = str(oneMonth)

        if(oneMonth < 10):
            mon = '0' + mon

        mon = str(dateInput)[2:] + mon

        dateRange.append(mon)
    break


def date_converter(input):    # 트위터 시간(샌프란시스코)을 한국 시간으로 변환하는 함수
    # from datetime import datetime, timedelta
    now = input

    ampm = str(now).split(' ')[0]
    dateNow = ''
    isPM = False
    
    if(now.find('오전 12') != -1):
        now = now.replace('오전 12','오전 00')

    if(ampm == '오전'):
        dateNow = now.replace('오전 ', '')
    elif(ampm == '오후'):
        dateNow = now.replace('오후 ', '')
        isPM = True
    
    c_dateNow = datetime.strptime(dateNow, '%H:%M - %Y년 %m월 %d일')
    
    parallax = timedelta(hours = 16)
    pm_to_am = timedelta(hours = 12)
    
    c_dateNow += parallax
    
    if(isPM):
        c_dateNow += pm_to_am
    
    return c_dateNow

def inputDate_to_searchTxt(inputDate):    # '1701' 형식의 연월이 입력되면 검색어를 리턴 (since:17-01-01 until:17-01-31 from:poltra055)
    print(inputDate)
    
    since = '20' + inputDate + '01'
    until = '20' + inputDate
    
    until += str(calendar.monthrange(int(until[:4]), int(until[4:]))[1])

    result = 'since:'+ since[:4] + '-' + since[4:6] + '-' + since[6:]
    result += ' until:' + until[:4] + '-' + until[4:6] + '-' + until[6:]
    result += ' from:poltra055'
    
    return result


os.path.join(os.path.dirname(__file__))
dir_path = os.path.dirname(os.path.realpath(__file__))    # 현재 실행중인 이 파일의 위치를 dir_path에 저장


if not(os.path.isdir(dir_path + '/' + dateInput)):    # 만약 연도 폴더가 없을 경우 새로 생성
        os.makedirs(os.path.join(dir_path + '/' + dateInput))

# 크롬 드라이버를 사용해서 웹 브라우저를 실행
path = dir_path + "/chromedriver.exe"
driver = webdriver.Chrome(path)

dir_path = dir_path + '/' + dateInput

for oneMonth in dateRange:

    if(os.path.isfile(dir_path + '/' + oneMonth + '.xls')):
        continue

    url = 'https://twitter.com/search?q=' + inputDate_to_searchTxt(oneMonth) + '&src=typd'

    driver.get(url)
    time.sleep(3)    # 사이트가 열릴 때까지 대기

    full_html = driver.page_source
    soup = BeautifulSoup(full_html, 'html.parser')    # 현재 페이지 html 소스 전체를 문자로 변환하여 soup 변수에 저장

    contents = []
    daytimes = []

    twitIndex = 0

    twit_list = soup.find('ol', class_ = 'js-navigable-stream').find_all('li', class_ = 'js-stream-item')

    while(True):
        print("현재 화면상의 트윗 갯수 : " + str(len(twit_list)))

        while(True):
            twit = twit_list[twitIndex]

            twitTxtOrg = str(twit.find('p', class_ = 'js-tweet-text').get_text()).split('#')[0].strip().split('\n')
            twitTxt = ""

            for t in twitTxtOrg:
                twitTxt += t.strip() + " "

            twitTime = date_converter(str(twit.find('a', class_ = 'tweet-timestamp')['title']))

            contents.append(twitTxt)
            daytimes.append(twitTime)

            twitIndex += 1
            print(oneMonth + ')', str(twitIndex) + "번째 트윗 완료")

            if(twitIndex == len(twit_list)):    
                break

        isPageEnd = False    # 마지막인지 체크

        for i in range(0,5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")    # 스크롤 다운
            time.sleep(2)    # 스크롤 후 대기시간.

            full_html = driver.page_source
            soup = BeautifulSoup(full_html, 'html.parser')

            new_list = soup.find('ol', class_ = 'js-navigable-stream').find_all('li', class_ = 'js-stream-item')

            if(len(new_list) != len(twit_list)):
                twit_list = new_list
                print('스크롤 다운 & 새로운 트윗 로드')
                continue
            else:
                isPageEnd = True
                break
        
        if(isPageEnd):
            break

    contents.reverse()
    daytimes.reverse()

    all_twit = pd.DataFrame()
    all_twit['내용'] = contents
    all_twit['날짜'] = daytimes

    f_path = dir_path + '/' + oneMonth + '.xls'
    all_twit.to_excel(f_path)

    print(oneMonth + ' 엑셀파일 저장')
    print('\n저장한 트윗 수 : ' + str(twitIndex) + '\n')
    continue


print('모든 작업이 끝났습니다.')