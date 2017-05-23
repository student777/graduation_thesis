# What is this?
Analysis on:  
1) subway traffic in Seoul - visualization
2) real estate price in Seoul - visualization
3) traffic vs price - regression  
This is part of my graduation thesis..  

# Examples
files at out_example/ 

1) hourly traffic(ride/alight)  
![](http://blog.wisebear.xyz/wp-content/uploads/2017/05/설입.png)

2) traffic map(ride)  
![](http://blog.wisebear.xyz/wp-content/uploads/2017/05/ride2.png)

3) traffic map(alight)  
![](http://blog.wisebear.xyz/wp-content/uploads/2017/05/alight2.png)

4) traffic map(total, grid)  
![](http://blog.wisebear.xyz/wp-content/uploads/2017/05/grid2.png)  

5) price map  
![](http://blog.wisebear.xyz/wp-content/uploads/2017/05/price2.png)  


# Resources  
**res/station_location.csv**  
ref) http://data.seoul.go.kr/openinf/sheetview.jsp?infId=OA-118&tMenu=11  
**res/price_{housing_type}_201701.xlsx**  
ref) http://rtdown.molit.go.kr  
1) single_trade: 단독다가구(매매)  
2) single_rent: 단독다가구(전월세)  
3) apartment_trade: 아파트(매매)  
4) apartment_rent: 아파트(전월세)   
5) officetel_trade: 오피스텔(매매)   
6) officetel_rent: 오피스텔(전월세)   
7) multi_trade: 연립다세대(매매)   
8) multi_rent: 연립다세대(전월세)   
9) land_trade: 토지(매매)   


# To do
Regression: price ~ address + area + year_built  s.t. address = f('**구', '**동')  
Grid: square -> pentagon  


# Required python library  
matplotlib  
numpy  
xlrd  
gmplot  
