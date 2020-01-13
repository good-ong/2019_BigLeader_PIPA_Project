library(ggmap)

data <- read.csv("place.csv", header = TRUE, fileEncoding = "utf-8") 

register_google(key='AIzaSyD2W5DqsBHQRCy4DMFY0CikIEQlxTFYVgE')
data$address <- enc2utf8(data$address) ## 인코딩 처리 안돌아가도 되더라
data$address <- as.character(data$address)
data_lonlat <- mutate_geocode(data, address, source='google') ##위경도 변호호출
write.csv(data_lonlat, "cleaning_data.csv", row.names = TRUE) ## csv export