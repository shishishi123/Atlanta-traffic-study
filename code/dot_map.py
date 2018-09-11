from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


fig=plt.figure(figsize=(11,8))
# 绘制基础地图，选择绘制的区域，因为是绘制美国地图，故选取如下经纬度，lat_0和lon_0是地图中心的维度和经度
map = Basemap(projection='lcc',lat_0=33.5,lon_0=-84.5,\
            llcrnrlat=33 ,urcrnrlat=34.5,\
            llcrnrlon=-85.2,urcrnrlon=-83.7,\
            resolution='l'
            )
map.drawmapboundary()   # 绘制边界
map.drawstates()        # 绘制州
map.drawcoastlines()    # 绘制海岸线
map.drawcountries()     # 绘制国家
map.drawcounties()      # 绘制县
map.bluemarble(scale=0.5)
map.etopo(scale=0.6, alpha=0.6)

posi=pd.read_csv("total_data_of_georgia.csv") # 读取数据

lat = np.array(posi["weidu"])                        # 获取维度之维度值
lon = np.array(posi["jingdu"])                        # 获取经度值
pop = np.array(posi["AADT"],dtype=float)    # 获取人口数，转化为numpy浮点型

size=(pop/np.max(pop))*50     # 绘制散点图时图形的大小，如果之前pop不转换为浮点型会没有大小不一的效果
x,y = map(lon,lat)

map.scatter(x,y,s=size,c=(0.7,0,0.8))     # 也可以使用Basemap的methord本身的scatter
plt.title('Traffic in Fulton')
plt.savefig('georgia_dot_map.png')
plt.show()