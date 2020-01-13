# ===================================================================================
# ===================================================================================

# ** 사용자 변수 **
# 여기 있는 변수만 조절해서 전체코드 돌리면 됩니다

# 파일 경로 폴더
path = "C:\\Users\\gkstm\\Desktop\\민원 플랫폼\\R코드+csv파일"

# csv 파일 이름
file = "토탈키워드.csv"


# 워드클라우드 만들 단어 수 (csv 파일 최대 행 길이를 넘기면 전체 단어로 함)
word_num = 200


# 포인트를 줄 키워드
# keywords = c('주차', '차량', '도로', '무단', '교통', '시설')
keywords = readLines('키워드.txt', encoding = 'UTF-8')


# 워드클라우드 배경색 / 기본 글자색 / 포인트 글자색 (hex코드도 가능)
# 아래 링크 참고하면 좋음
# https://www.google.com/search?ei=epE_XfirHJeJoATr_Y7ADw&q=hex+color
background_color = 'white'
base_word_color = '#17375e'
point_word_color = '#ffaf0f'


# 포인트 준 키워드도 흐리게 할 것인지
# (기본 FALSE - 키워드는 빈도수가 작아도 흐려지지 않음)
is_pointed_word_fade = F


# 실제 단어빈도수를 반영할 것인지
# (기본 FALSE - 빈도 순서만 가져오고 빈도수는 로그함수로 대체하여 적당히 보기 좋게 만들어줌)
is_real_freq = F

# ===================================================================================
# ===================================================================================


# <데이터 밑준비> 
setwd(path)
library(wordcloud2)
input <- data.frame(read.csv(file))

if(class(input[,1]) == 'integer'){
  input = input[,c(2,3)]
}

if(nrow(input) > word_num){
  input = input[1:word_num,]
}


# 포인트 줄 단어들을 찾기
point_word = rep(F, nrow(input))

for(i in 1:length(keywords)){
  point_word[grep(keywords[i],input[,1])] = T
}
point_word

# r, g, b값(0~255)을 입력하면 hex code로 바꿔주는 함수
rgb2hex <- function(r,g,b) rgb(r, g, b, maxColorValue = 255)

# 글자색을 지정하는 함수
# 기본색과 포인트색으로 나눔
# 빈도수가 낮을수록 색이 옅어짐 (즉 배경색에 가까워짐)
setColor = function(){
  
  base_col = base_word_color
  point_col = point_word_color
  
  # col2rgb를 쓰면 헥스코드를 c(r,g,b) 형태의 벡터를 반환함
  # 1,2,3 대신 r,g,b로 인덱싱하도록 만들어서 직관성 높임
  r = 1
  g = 2
  b = 3
  
  
  # 만약 데이터셋 길이만큼 seq를 해주면 빈도가 낮은 글자들은 색이 너무 옅어짐
  # 그래서 데이터셋 길이에 적당한 값(w)을 곱해서 적당히 너무 옅어지지 않도록 함
  w = 1.2
  length_w = nrow(input) * w
  
  
  # background color
  bg_col = col2rgb(background_color)
  
  
  # base color
  b_col = col2rgb(base_col)
  
  b_r = b_col[r]
  b_g = b_col[g]
  b_b = b_col[b]

  
  tmp_b_r = seq_new(b_r, bg_col[r], abs(bg_col[r] - b_r) / length_w )  
  tmp_b_g = seq_new(b_g, bg_col[g], abs(bg_col[g] - b_g) / length_w )
  tmp_b_b = seq_new(b_b, bg_col[b], abs(bg_col[b] - b_b) / length_w )
  
  color_column = rgb2hex(tmp_b_r,tmp_b_g,tmp_b_b)[1:nrow(input)]
  
  
  # point color
  p_col = col2rgb(point_col)
  
  p_r = p_col[r]
  p_g = p_col[g]
  p_b = p_col[b]
  
  if(is_pointed_word_fade == T){
    tmp_p_r = seq_new(p_r, bg_col[r], abs(bg_col[r] - p_r) / length_w )  
    tmp_p_g = seq_new(p_g, bg_col[g], abs(bg_col[g] - p_g) / length_w )
    tmp_p_b = seq_new(p_b, bg_col[b], abs(bg_col[b] - p_b) / length_w )
  }
  else{
    tmp_p_r = rep(p_r, length_w )  
    tmp_p_g = rep(p_g, length_w )
    tmp_p_b = rep(p_b, length_w )
  }
  
  tmp_p = rgb2hex(tmp_p_r,tmp_p_g,tmp_p_b)[1:nrow(input)]
  
  print(color_column[point_word == T])
  print(tmp_p[point_word == T])
  
  color_column[point_word == T] = tmp_p[point_word == T]
  
  return(color_column)
}

seq_new = function(start,end,by){
  
  if(start > end){
    result = seq(end,start,by)
    result = sort(result,decreasing = T)
  }
  else{
    result = seq(start,end,by)
  }
  return (result)
  
}


# 글자수 조절
# 로그함수 써서 적당히 보기 좋게 만들어준다
if(is_real_freq == F){
  input[,2] = log_y = 6-log(c(3:202))
}
# log_y = 6-log(c(4:203))
# plot(log_y)


# 글자색상칼럼 추가
input$col = setColor()


View(input)
plot(c(1:nrow(input)), input[,2])


# 동그라미
wordcloud2(input[,1:2],
           gridSize=6, 
           size = .4, 
           shape = 'circle',
           backgroundColor = background_color,
           color=input$col,
           rotateRatio = 0,
           ellipticity = 0.8)

# 네모인데 단어수가 적어서 그런지 동그라미랑 별 차이 없음
wordcloud2(input[,1:2],
           gridSize=6, 
           size = .4, 
           shape = 'sqare',
           backgroundColor = background_color,
           color=input$col,
           rotateRatio = 0,
           ellipticity = 0.8)

# 오각형
wordcloud2(input[,1:2],
           gridSize=6, 
           size = .4, 
           shape = 'pentagon',
           backgroundColor = background_color,
           color=input$col,
           rotateRatio = 0,
           ellipticity = 0.8)


# figPath 옵션 사용해서 그림 모양으로 워드클라우드 돌려보려 했는데 잘 안됨
# 구글링해봐도 안된다는 글만 많고 해결책이라고 올라온거 다 시도해봤는데 안됨
# (devtools로 패키지 설치하기, 크롬말고 다른 브라우저 쓰기, RStudio말고 R에서 실행 등등등)