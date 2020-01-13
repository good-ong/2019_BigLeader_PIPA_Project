# 라이브러리
library(readxl)
library(NbClust)

# 디렉토리 설정 및 데이터 불러오기
setwd("c:/users/rbehd/desktop/")
data <- read_excel("signature_table.xlsx")

# 데이터 전처리(음의 상관관계에 있을법한 변수들에 대해 max값을 빼주어 양의 상관관계로 재정의)
data$parking_pay <- ifelse(data$parking_pay=="무료", 1, 0)
data$parking_time <- ifelse(data$parking_time=="24시간", 1, 0)
data$parking_area <- max(data$parking_area)-data$parking_area
data$C <- max(data$C)-data$C
data$D <- max(data$D)-data$D
data$floating_people <- max(data$floating_people)-data$floating_people

# 원하는 데이터만 가져오기
newdata <- data.frame(dansok=data$D, zone=data$parking_area, pay=data$parking_pay, time=data$parking_time,
                      cctv=data$C, pop=data$floating_people)

# 비계층적 군집분석 (kmeans)
nc <- NbClust(newdata, min.nc = 2, max.nc = 15, method = "kmeans")
par(mfrow=c(1,1))
barplot(table(nc$Best.nc[1,]),xlab="Numer of Clusters", ylab="Number of Criteria",
        main="Number of Clusters Chosen")
cluster <- kmeans(newdata, centers = 3, iter.max = 10000)

# 계층적 군집분석(h-clust)
dist = dist(newdata, method="euclidean")
hc = hclust(dist)
plot(hc)
rect.hclust(hc, k=3, border = "red")
ghc = cutree(hc, k=3)

newdata$kmeans <- cluster$cluster
newdata$ghc <- ghc

cor(newdata$kmeans, newdata$ghc)