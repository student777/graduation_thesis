# What is this?
Analysis on:  
1) subway traffic in Seoul - visualization
2) real estate price in Seoul - visualization
3) traffic vs price - regression  
This is part of my graduation thesis..  

# Required python library  
matplotlib  
numpy  
xlrd  
gmplot  

# To do
Regression: price ~ address + area + year_built  s.t. address = f('**구', '**동')  
Grid: square -> pentagon  

# Resources  
## res/station_location.csv  
ref) http://data.seoul.go.kr/openinf/sheetview.jsp?infId=OA-118&tMenu=11  
## res/price_{housing_type}_201701.xlsx  
ref) http://rtdown.molit.go.kr  
single_trade: 단독다가구(매매)  
single_rent: 단독다가구(전월세)  
apartment_trade: 아파트(매매)  
apartment_rent: 아파트(전월세)   
officetel_trade: 오피스텔(매매)   
officetel_rent: 오피스텔(전월세)   
multi_trade: 연립다세대(매매)   
multi_rent: 연립다세대(전월세)   
land_trade: 토지(매매)   