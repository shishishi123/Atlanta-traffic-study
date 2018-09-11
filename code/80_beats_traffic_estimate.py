import pandas as pd
import folium
import webbrowser

station_data=pd.read_csv('beats_data.csv')
station_data_matrix=station_data.values
def station_ID_preprocess(data_matrix):
    for data_1 in data_matrix:
        data_list = []
        for data_2 in data_1:
            if type(data_2)!=float:
                data_list.append(data_2)
        yield data_list
generater=station_ID_preprocess(station_data_matrix)

AADT_data=pd.read_csv('Atlanta_data_plus.csv')
AADT_data_matrix=AADT_data.values

traffic_load=[]

def get_traffic_load(list_of_sensor,data_matrix):
    traffic_load=0
    for sensor_ID in list_of_sensor:
        for item in data_matrix[:,]:
            if sensor_ID==item[0]:
                traffic_load=traffic_load+item[3]

    return traffic_load

for data_list in generater:
    loads=get_traffic_load(data_list,AADT_data_matrix)
    traffic_load.append(int(loads))

print(traffic_load)