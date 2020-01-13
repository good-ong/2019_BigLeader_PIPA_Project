from bs4 import BeautifulSoup    # html 소스를 전부 가져오는 기능
from selenium import webdriver    # 브라우저 실행 및 검색창, 버튼 조작
import time    # 페이지 열기에 필요한 시간만큼 대기하는 기능
import sys    # 파일 작성할 때 필요
import os    # 경로 설정할 때 필요
import pandas as pd    # 데이터프레임 작성
import xlwt    # 데이터프레임을 엑셀파일로 저장
from datetime import datetime    # 날짜
import math    # ceil 함수

print('=' * 120)
print("""
              ::::::::::::.                   ..::::.
            =:            .+               :=:       .::.
           +   .:::::=      =             =.    :::::.  .+
          .:   +      +     =            +     +      =   +
           =   +.....:..:::=.:::::::::::::=::. =       +  =
           +      :.                         .: :::::::.  :.
           .=  :::                                        +
            :+:          .                         .    .=
          .=            @#           @             :+.::.
         =:            =@=          *@              .:
        +               .           .:               +
      .=                                             +
     .=                                              +
     +             :::.@@@*.::::                    :.
    :.           := :  .+       .=                 :=
    :.          ::  :::::::+      +             :::
     +          +                 +        :::::
      :::::::::.*.:::::::::::::::.+.::::::.
""")

print('  교통정보 크롤러')

print('=' * 120)



# 현재 실행중인 이 코드파일의 위치를 dir_path에 저장
# 사용자마다 크롬 드라이버 위치가 제각각일 수 있어요
# 그래서 이 코드파일이랑 같은 폴더에 첨부된 드라이버를 사용하도록 하는 것입니다
# 저장도 같은 폴더에 하니까 찾기 편해요
os.path.join(os.path.dirname(__file__))
dir_path = os.path.dirname(os.path.realpath(__file__))


# 크롬드라이버 실행
path = dir_path + "/chromedriver.exe"
driver = webdriver.Chrome(path)


    
# 제목과 날짜, 조회수를 저장할 리스트
kind = []
start = []
end = []
speed = []

full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')    


while(True):

    for page in range(start_page, hope_page + 1):
        
        # 정석대로라면 앞에서 쓴 것처럼 사이트 열고 검색칸 찾아서 검색어 넣고 검색버튼 클릭하고
        # 페이지 루프하면서 크롤링하는 게 맞아요
        # 근데 네이버는 API 사용하듯이 page= 파라미터만 바꾸면 페이지 이동이 돼요
        # 그래서 페이지 수로 for문 돌렸어요
        # 앙 개꿀띠
        
        url = 'https://cafe.naver.com/' + cafe_dic[cafe_num_real][0] + '?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=14793916%26search.media=0%26search.searchdate=all%26search.exact=%26search.include=%26userDisplay=50%26search.exclude=%26search.option=0%26search.sortBy=date%26search.searchBy=1%26search.includeAll=%26search.query=%C1%D6%C2%F7%26search.viewtype=title%26search.page='
        url += str(page)

        driver.get(url)
        time.sleep(2)

        driver.switch_to_default_content()


        # 현재 페이지의 iframe 체크 (그냥 확인용)
        # 이런 식으로 현재 페이지에 어떤 iframe이 있는지 간단히 확인해볼 수 있어요
        iframes = driver.find_elements_by_css_selector('iframe')
        for iframe in iframes:
            print(iframe.get_attribute('name'))

        
        # iframe 이동
        driver.switch_to_frame("cafe_main")
        
        time.sleep(5)

        # 현재 페이지 html 소스 전체를 문자로 변환하여 soup 변수에 저장
        full_html = driver.page_source
        soup = BeautifulSoup(full_html, 'html.parser')    


        # 글목록 tr 태그들을 찾아서 content_list에 저장
        # find로 찾으면 안돼요.. 클래스명까지 완전히 똑같은 태그가 여러 개 있어요
        # select 주소 찾는 법 : xpath 복사하는 것처럼 selector를 복사한 후
        # nth-child를 nth-of-type로 바꿔주면 됩니다
        # select는 조건을 만족하는 모든 태그들을 리스트로서 저장하고
        # select_one은 하나만 저장해요
        content_list = soup.select('#main-area > div:nth-of-type(5) > table > tbody > tr')

        
        # 마지막 페이지인지 체크
        # 만약 이 페이지의 글이 50개 미만이라면 이 페이지가 마지막 페이지란 뜻일 거에요
        # 그러면 이번 페이지가 끝나고 나서 break를 해줘요
        is_last_page = False
        if(len(content_list) < 50):
            is_last_page = True


        # 이 부분은 복잡해서 주석으로 설명하기가 어려워요
        # 하나하나 설명하면 코드가 너무 길어지고 지저분해질 것 같아서요
        # 혹시 설명이 필요하다면 말해주세요
        for tr in content_list:

            num_cnt += 1
            
            print('*' * 100)

            # 글 제목 가져오기
            title_txt_source = tr.find('a', class_='article')
            title_txt = ''
            if(str(type(title_txt_source)) == "<class 'NoneType'>"):
                print('논타입')
                title_txt_source = BeautifulSoup(str(title_txt_source), "lxml")

            for t in title_txt_source:
                if(str(type(t)) == "<class 'bs4.element.NavigableString'>"):
                    stripped_text = t.strip()

                    if(t.find(stripped_text) == -1):
                        title_txt += remove_space(t)
                    elif(t.find(stripped_text) > 5):
                        title_txt += remove_space(t,'l')
                    else:
                        title_txt += remove_space(t,'r')


                elif(str(type(t)) == "<class 'bs4.element.Tag'>"):

                    if(t.text.find('[') != -1):
                        continue
                    else:
                        title_txt += remove_space(t.text)
            
            # 날짜 가져오기
            date_txt_source = tr.find('td',class_='td_date')
            
            if(str(type(date_txt_source)) == "<class 'NoneType'>"):
                print('논타입')
                date_txt_source = BeautifulSoup(str(date_txt_source), "lxml")

            date_txt = date_txt_source.text

            # 오늘 올라온 글은 날짜가 아닌 시간으로 표시되기 때문에 오늘 날짜로 변경
            if(len(date_txt) < 11):
                now = datetime.now()
                date_txt = str(now.year) + '.' + '%02d'%now.month + '.' + '%02d'%now.day + '.'


            # 조회수 가져오기
            read_txt_source = tr.find('td', class_='td_view')
            
            if(str(type(read_txt_source)) == "<class 'NoneType'>"):
                print('논타입')
                read_txt_source = BeautifulSoup(str(read_txt_source), "lxml")

            read_txt = read_txt_source.text.replace(',','')


            print(cafe_dic[cafe_num_real][1] ,num_cnt,':',title_txt,date_txt)
            title.append(title_txt)
            date.append(date_txt)
            read.append(read_txt)

            # 현재 페이지 수가 원하는 검색 건수와 같으면 루프 break
            if(num_cnt == hope_num):
                break
        
        # 원하는 검색 건수에 도달했거나 지금이 마지막 페이지라면 break
        if(num_cnt == hope_num or is_last_page):
            break

        
    sheet = pd.DataFrame()
    sheet['제목'] = title
    sheet['날짜'] = date
    sheet['조회수'] = read

    f_path = dir_path + '/' + cafe_dic[cafe_num_real][1] + '_' + str(datetime.now()).split('.')[0].replace(':','').replace(' ','_') + '.xls'
    sheet.to_excel(f_path)

    if(is_all and cafe_num_real < 5):
        num_cnt = start_num - 1
        cafe_num_real += 1
        title = []
        date = []
        read = []
    else:
        break
        

print('\n모든 작업이 끝났습니다.')