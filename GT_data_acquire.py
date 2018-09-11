import requests
from bs4 import BeautifulSoup
import bs4
import pandas as pd

def getURL(cosit):
    dates={
        '2018-01-01':'2018-01-31',
        '2018-02-01':'2018-02-28',
        '2018-03-01':'2018-03-31',
        '2018-04-01':'2018-04-30',
        '2018-05-01':'2018-05-31',
        '2018-06-01':'2018-06-30',
        '2018-07-01':'2018-07-31',
        '2018-08-01':'2018-08-31',
        '2018-09-01':'2018-09-30',
        '2018-10-01':'2018-10-31',
        '2018-11-01':'2018-11-30',
        '2018-12-01':'2018-12-31'
    }
    for reportdate,enddate in dates.items():
        temp='https://gdottrafficdata.drakewell.com/tfdaysreport.asp?node=GDOT_CCS&cosit='+cosit+'&reportdate='+reportdate+'&enddate='+enddate+'.html'
        yield temp

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(html,data_num):
    soup = BeautifulSoup(html, "html.parser")
    num=0
    for tr in soup.find('table').children:
        if num<24:
            if isinstance(tr, bs4.element.Tag) and tr!=[]:
                tds = tr('td')
                if tds!=[]:
                    for i in range(data_num):
                        yield tds[i+1].string
                    num=num+1

def station_ID_preprocess(data_matrix):
    station_list=[]
    for data_1 in data_matrix:
        data_list = []
        i=0
        for data_2 in data_1:
            if type(data_2)!=float:
                if i==0:
                    data_list.append(data_2)
                else:
                    data_2=data_2[:3]+data_2[4:]
                    data_list.append('00000'+data_2)
            i=i+1
        station_list.append(data_list)
    return station_list

def main():
    station_data = pd.read_csv('station_data_2.csv')
    station_data_matrix = station_data.values
    date_generater = station_ID_preprocess(station_data_matrix)
    lenth_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for datas in date_generater[4:5]:
        cosits = datas[1:]
        for cosit in cosits:
            i=0
            urls = getURL(cosit)
            filepath = '2018newdata/' + str(datas[0]) + '.txt'
            for url in urls:
                html = getHTMLText(url)
                generater=fillUnivList(html,lenth_of_month[i])
                i=i+1
                with open(filepath, 'a') as fileobject:
                    for data in generater:
                        if data!='\xa0-':
                            fileobject.write(str(data))
                            fileobject.write(',')
                        else:
                            fileobject.write('0')
                            fileobject.write(',')
            with open(filepath, 'a') as fileobject:
                fileobject.write('\n')
            print('Yes')
        print('ok')
main()