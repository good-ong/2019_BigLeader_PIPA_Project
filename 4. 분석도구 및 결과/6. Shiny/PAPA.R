library(shiny)
library(shinydashboard)
library(leaflet)
library(leaflet.extras)
library(geosphere)
library(ggmap)
library(tableHTML)
library(leafem)


setwd('C:\\Users\\gkstm\\Desktop\\PIPA_data\\시그니쳐테이블')

cctv = read.csv('cctv_location.csv', encoding = 'cp949')
illegal = read.csv('단속건수.csv', encoding = 'cp949')


signature_table = read.csv('signature_table_real_final.csv', encoding = 'cp949')


cctv_group = 'CCTV'
illegal_group = '단속건수'
park_group = '주차장'


register_google(key='AIzaSyD2W5DqsBHQRCy4DMFY0CikIEQlxTFYVgE')



icon_parking = icon('parking', class = 'icon', lib = "font-awesome")
icon_adr = icon('home', class = 'icon', lib = 'font-awesome')
icon_grade = icon('star', class = 'icon', lib = 'font-awesome')
icon_ruler = icon('ruler-horizontal', class = 'icon', lib = 'font-awesome')

grade_color = c('#24c95b',  '#98c924',  '#edb818',  '#ed7418',  '#ed4318')
grade_list = c('A','B','C','D','F')



recommend_park = function(park_list){
  divs = c()
  
  
  if(is.null(park_list)){
    return(div(
      HTML('<font color="#000000"><b>
  <p style="margin-bottom:5px">반경 200m 이내에 주차장 정보가<br>
    없습니다!</p>
  </b></font>')
      )
    )
  }
  
  
  for(i in 1:nrow(park_list)){
    
    adr = as.character(park_list$park_adr_list[i])
    if(nchar(adr) > 17){
      a = substr(adr,1,17)
      adr = paste0(a,'..')
    }

    g = park_list$park_value_list[i]
    grade = HTML(paste0('주차가능등급(PPG) : </font><font color="',grade_color[g],'">',grade_list[g],'</color><font color="#000000">'))
    
    one_div = list(
    div(
      HTML('<font color="#000000"><b>'),p(style='margin-bottom:5px', park_list$park_name_list[i]),HTML('</font></b>'),
      HTML('<font color="#000000">'),p(icon_parking,paste0(' 전체 주차면 : ',park_list$park_area_list)),HTML('</font>'),
      HTML('<font color="#000000">'),p(icon_adr,paste0(' ',adr)),HTML('</font>'),
      HTML('<font color="#000000">'),p(icon_ruler,paste0(' 거리: ',round(park_list$dist_list[i],2),' m')),HTML('</font>'),
      HTML('<font color="#000000">'),p(style='margin-bottom:25px',icon_grade,grade),HTML('</font>')
      
      
    ))
    divs = c(divs,one_div)
    
  }
  return(div(class='park_list',
    divs))
}



b = '경상남도 창원시 의창구 원이대로'
nchar(b)
substr(b,1,17)


a = get_close_park_list(cbind(128.6812436,35.2214879))
recommend_park(a)
a





b = signature_table$parking_adr[70]
class(b)
as.character(b)

get_close_park_list = function(my_pos){
  # my_pos = cbind(lon,lat)
  
  park_index = c()
  dist_list = c()
  
  
  for(i in 1:nrow(signature_table)){
    park_pos = cbind(signature_table$parking_lng[i],signature_table$parking_lat[i])
    
    dist = distm(park_pos,my_pos)
    
    
    if(dist < 200){
      park_index = c(park_index,i)
      dist_list = c(dist_list,dist)
    }
  }
  
  park_name_list = c()
  park_area_list = c()
  park_adr_list = c()
  park_value_list = c()
  
  for(i in 1:length(park_index)){
    park_name = as.character(signature_table$parking_name[park_index[i]])
    park_name_list = c(park_name_list, park_name)
    
    park_area = signature_table$parking_area[park_index[i]]
    park_area_list = c(park_area_list,park_area)
    
    park_adr = as.character(signature_table$parking_adr[park_index[i]])
    park_adr_list = c(park_adr_list,park_adr)
    
    park_value = signature_table$ppr[park_index[i]]
    park_value_list = c(park_value_list,park_value)
  }
  
  if(length(park_name_list) < 1){
    sheet = NULL
  }else{
    
    sheet = data.frame(park_name_list,dist_list,park_area_list,park_adr_list,park_value_list)
    sheet = sheet[order(sheet$dist_list),]
    
    if(nrow(sheet) > 5){
      sheet = sheet[1:5,]
    }
  }
  return(sheet)
}


park_marker = iconList(
  makeIcon(iconUrl = 'icon/park_marker_1.png',iconAnchorX = 20, iconAnchorY = 40),
  makeIcon(iconUrl = 'icon/park_marker_2_2.png',iconAnchorX = 20, iconAnchorY = 40),
  makeIcon(iconUrl = 'icon/park_marker_3.png',iconAnchorX = 20, iconAnchorY = 40),
  makeIcon(iconUrl = 'icon/park_marker_4_2.png',iconAnchorX = 20, iconAnchorY = 40),
  makeIcon(iconUrl = 'icon/park_marker_5.png',iconAnchorX = 20, iconAnchorY = 40)
)

legend_icon = iconList(
  makeIcon(iconUrl = 'icon/legend_cctv.png'),
  makeIcon(iconUrl = 'legend_illegal.png')
)


ui = dashboardPage(
  skin='red',
  
  dashboardHeader(
    title = 'PAPA'
  ),
  
  dashboardSidebar(
    width = 300,
    
    sidebarMenu(
      
      # tags$head(tags$style(HTML('
      # .form-group, .selectize-control {
      #      margin-bottom: 0px;
      # }
      # .box-body {
      #     padding-bottom: 0px;
      # }'))),

      menuItem("내 위치 찾기", tabName = "get_position", icon = icon("location-arrow"),startExpanded = T,
               
               HTML('<p style="padding:10px"><font size="2" color="gray">
                    ※ 주소 / 위도경도 중 택일하여 입력 후<br>
                    [위치 찾기] 버튼을 클릭하시면 됩니다.<br>
                    둘 다 입력되어 있으면 주소 입력을 우선합니다.<br>
                    입력이 잘못되었으면 기본 위치(창원시청)를<br>
                    보여줍니다.
                    </font></p>'),
              
               menuItem('주소로 찾기',tabName='by_adr',
                           textInput('address', '주소', "경상남도 창원시 의창구 시청")
                           ),
               
               menuItem('위도경도로 찾기',tabName='by_lonlat',
                           fluidRow(
                                column(5,style="padding:0",numericInput('latitude', '위도', 35.2279246, min = 35, max = 36)),
                                column(5,style="padding:0",numericInput('longtitude', '경도', 128.6812436, min = 128, max = 129))
                              )
                           ),
              
               div(
                  style="text-align:right; width:100%; padding-above:0;",
                  actionButton(inputId = "now_place",
                               label = "위치 찾기",
                               style = "display:inline")
                   )
                )
      
      ),
      br(),
      box(title = '주차장 추천',
          width = 12,
          #height = 600,
          status = "warning",
          
          solidHeader = TRUE,
          collapsible = TRUE,
          
          htmlOutput('recommend')

          )
      ),
  

  
  dashboardBody(
    
    tags$style(type = "text/css", "#mymap {height: calc(100vh - 80px) !important;}"),
    leafletOutput("mymap")
    
  )
)


get_pos = function(adr, lonlat){
  
  if(adr=="" & (is.na(lonlat[1]) | is.na(lonlat[2]))){
    print(1)
    return(cbind(128.6812436,35.2279246)) # 둘 다 없을 경우 기본값(창원시청)
    
  }else if((is.na(lonlat[1]) | is.na(lonlat[2]))){
    print(2)
    lonlat = geocode(adr, source='google')
    print(cbind(as.numeric(lonlat[1]),as.numeric(lonlat[2])))
    return(cbind(as.numeric(lonlat[1]),as.numeric(lonlat[2])))
    
  }else if(adr==""){
    print(3)
    print(lonlat)
    return(lonlat)
    
  }else{
    print(4)
    lonlat = geocode(adr, source='google')
    print(cbind(as.numeric(lonlat[1]),as.numeric(lonlat[2])))
    return(cbind(as.numeric(lonlat[1]),as.numeric(lonlat[2])))
  }
}

adr = '경상남도 창원시 의창구 시청'
lonlat = cbind(128.6812436,35.2279246)
a = get_pos(adr,lonlat)
class(a[2])
as.numeric(a[2])

server = function(input, output) { 
  
  point = eventReactive(
    input$now_place,
    { get_pos(input$address, cbind(input$longtitude, input$latitude)) },
    ignoreNULL = FALSE)
  
  output$mymap = renderLeaflet({
    m = leaflet(illegal) %>%
      addWebGLHeatmap(lng=~lon,lat=~lat,size=250,layerId='heatmap',group=illegal_group, opacity = 0.5) %>%
      addProviderTiles(
        providers$OpenStreetMap,
        options = providerTileOptions(noWrap = TRUE)) %>%
        addMarkers(data = point(), popup=paste0("현재 위치: <br>",point()[1],", ",point()[2])) %>%
        addCircles(point()[1],point()[2],
                   radius = 200,
                   weight = 0.5,
                   opacity = 0.7,
                   fillOpacity = 0.5,
                   fillColor = 'skyblue',
                   color = 'blue') %>%
        setView(point()[1],point()[2], zoom = 16)
      
    for(i in 1:nrow(cctv)){
      lat = cctv$위도[i]
      lon = cctv$경도[i]
      
      for(i in 1:length(cctv$대수[i])){
        m = addCircles(map = m,
                       lng = lon,
                       lat = lat,
                       radius = 100,
                       group = cctv_group,
                       weight = 0.1,
                       opacity = 0.3,
                       fillOpacity = 0.5,
                       fillColor = 'red')
        
        m = addCircles(map = m,
                       lng = lon,
                       lat = lat,
                       radius = 5,
                       group = cctv_group,
                       weight = 0,
                       opacity = 0.7,
                       fillOpacity = 1,
                       fillColor = 'red',
                       color = 'red')
      }
    }
    
    for(i in 1:nrow(signature_table)){
      
      lat = signature_table$parking_lat[i]
      lon = signature_table$parking_lng[i]
      
      var = signature_table$ppr[i]
      c = paste0('<font color="',grade_color[var],'">',grade_list[var],"</font>")
      
      pay_color = ''
      if(signature_table$parking_pay[i] == '무료'){
        pay_color = '#54c472'
      }else{
        pay_color = '#c45472'
      }
      
      m = addMarkers(map = m,
                     lng = lon,
                     lat = lat,
                     icon = park_marker[signature_table$ppr[i]],
                     group = park_group,
                     popup = paste0('<font size=4>',
                       '<b>',signature_table$parking_name[i],'</b>','<br>',
                       signature_table$parking_adr[i],'<br>','<br>',
                       paste('전체주차면 :',signature_table$parking_area[i]),'<br>','<br>',
                       paste('주차가능시간 :',signature_table$parking_time[i]),'<br>','<br>',
                       '<font color="',pay_color,'">',signature_table$parking_pay[i],'</font>','<br>','<br>',
                       paste('주차가능등급(PPG) :',c),'</font>'
                     )
      )
    }

    m = addLayersControl(map = m,
                     overlayGroups = c(cctv_group, park_group, illegal_group),
                     options = layersControlOptions(collapsed = FALSE)
                    )
    
    m = addMouseCoordinates(m)
    
    
    # m = m %>% hideGroup(illegal_group) %>% hideGroup(cctv_group)

    })

  
  
  park_list = eventReactive(
    input$now_place,
    { get_close_park_list(cbind(point()[1],point()[2])) },
    ignoreNULL = FALSE)
  
  
  output$recommend = renderUI({
    
    recommend_park(park_list())
    
    })
}







shinyApp(ui, server)

