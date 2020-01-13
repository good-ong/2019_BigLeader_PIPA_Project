import pandas as pd
import xlwt
import os

print('=' * 80)
print('  크롤링한 트윗 엑셀파일들을 하나로 합치는 프로그램입니다.')
print('  각 연도별 폴더에 있는 엑셀 파일들을 연도별로 하나의 파일로 합칩니다.')
print('=' * 80)


os.path.join(os.path.dirname(__file__))
dir_path = os.path.dirname(os.path.realpath(__file__))

while(True):
    dateInput = input('<<대상 연도>>\n  2015~2019 범위에서 합치기를 할 연도를 입력해주세요.\n  (예시: 2017)\n')
    
    if(dateInput.isdecimal() == False):
        print('다시 입력해주세요.\n')
        continue
    
    if(int(dateInput) < 2015 or int(dateInput) > 2019):
        print('다시 입력해주세요.\n')
        continue

    if not(os.path.isdir(dir_path + '/' + dateInput)):
        print('선택한 연도의 폴더가 없습니다.\n')
        continue
    
    if(len(os.listdir(dir_path + "/" + dateInput)) == 0):
        print('선택한 연도의 폴더가 비어있습니다.\n')
        continue
    
    dir_path += '/' + dateInput

    break
print(dir_path)
xls_list = os.listdir(dir_path)

collector_cont = []
collector_time = []

for xls in xls_list:
    df = pd.read_excel(dir_path + '/' + xls)
    collector_cont.extend(df['내용'])
    collector_time.extend(df['날짜'])
    print(xls.split('.')[0] + '완료')

all_twit = pd.DataFrame()
all_twit['내용'] = collector_cont
all_twit['날짜'] = collector_time

f_path = dir_path + '/' + 'result_' + xls_list[0].split('.')[0] +  '-' + xls_list[len(xls_list) - 1].split('.')[0] + '.xls'
all_twit.to_excel(f_path)

print('\n엑셀파일 저장')