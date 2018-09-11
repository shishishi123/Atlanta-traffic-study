import requests
from bs4 import BeautifulSoup
import bs4
import numpy as np
import pandas as pd

def getURL(cosit):
    url=[]
    dates={
        '2018-01-01':'2018-01-31',
        '2018-02-01':'2018-02-28',
        '2018-03-01':'2018-03-31',
        '2018-04-01':'2018-04-30',
        '2018-05-01':'2018-05-31',
        '2018-06-01':'2018-06-30',
        '2018-07-01':'2018-07-31',
        '2018-08-01':'2018-08-19',
    }
    for reportdate,enddate in dates.items():
        temp='https://gdottrafficdata.drakewell.com/tfdaysreport.asp?node=GDOT_CCS&cosit='+cosit+'&reportdate='+reportdate+'&enddate='+enddate+'.html'
        url.append(temp)
    return url

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=40)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('table').children:
        if isinstance(tr, bs4.element.Tag) and tr!=[]:
            tds = tr('td')
            mlist=[]
            if tds!=[]:
                for i in range(len(tds)):
                    mlist.append(tds[i].string)
                if mlist!=[]:
                    ulist.append(mlist)



def list_type_exchange(ulist,lenth):
    uinfo=np.array([])
    if len(ulist)<40:
        for i in range(24):
            mlist=[]
            for j in range(lenth):
                if ulist[i][j+1] != '\xa0-':
                    mlist.append(int(ulist[i][j+1]))
                else:
                    mlist.append(0)
            templist=np.array(mlist)
            uinfo=np.append(uinfo,templist,axis=0)
            #np.append
    elif len(ulist)<80:
        for i in range(24):
            mlist1 = []
            mlist2 = []
            for j in range(lenth):
                if ulist[2*i][j+1]!='\xa0-':
                    mlist1.append(int(ulist[2*i][j+1]))
                else:
                    mlist1.append(0)
            templist1=np.array(mlist1)
            for j in range(lenth):
                if ulist[2*i+1][j+1]!='\xa0-':
                    mlist2.append(int(ulist[2*i+1][j+1]))
                else:
                    mlist2.append(0)
            templist2=np.array(mlist2)
            templist=templist1+templist2
            uinfo = np.append(uinfo, templist, axis=0)
    else:
        for i in range(24):
            mlist1 = []
            mlist2 = []
            mlist3=[]
            mlist4=[]
            for j in range(lenth):
                if ulist[4*i][j+1]!='\xa0-':
                    mlist1.append(int(ulist[4*i][j+1]))
                else:
                    mlist1.append(0)
            templist1=np.array(mlist1)
            for j in range(lenth):
                if ulist[4*i+1][j+1]!='\xa0-':
                    mlist2.append(int(ulist[4*i+1][j+1]))
                else:
                    mlist2.append(0)
            templist2=np.array(mlist2)
            for j in range(lenth):
                if ulist[4*i+2][j+1]!='\xa0-':
                    mlist3.append(int(ulist[4*i+2][j+1]))
                else:
                    mlist3.append(0)
            templist3=np.array(mlist3)
            for j in range(lenth):
                if ulist[4*i+3][j+1]!='\xa0-':
                    mlist4.append(int(ulist[4*i+3][j+1]))
                else:
                    mlist4.append(0)
            templist4=np.array(mlist4)
            templist=templist1+templist2+templist3+templist4
            uinfo = np.append(uinfo, templist, axis=0)
    return uinfo



def printUnivList(ulist):
    for rlist in ulist:
        print(rlist)


def data_transfer(uinfo):
    lenth_of_month = [31, 28, 31, 30, 31, 30, 31, 19, 30, 31, 30, 31]
    for i in range(8):
        for day in range(lenth_of_month[i]):
            for j in range(24):
                yield uinfo[j*lenth_of_month[i]+day]

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
    station_data = pd.read_csv('beats_data.csv')
    station_data_matrix = station_data.values
    generater = station_ID_preprocess(station_data_matrix)
    lenth_of_month = [31, 28, 31, 30, 31, 30, 31, 19, 30, 31, 30, 31]
    for datas in generater:
        cosits = datas[1:]
        for cosit in cosits:
            data_matrix = np.array([])
            templist = np.array([])
            i = 0
            urls = getURL(cosit)
            for url in urls:
                uinfo = []
                html = getHTMLText(url)

                fillUnivList(uinfo, html)
                uinfo=list_type_exchange(uinfo, lenth_of_month[i])

                templist=np.append(templist,uinfo,axis=0)
                i=i+1
            data_matrix=np.append(data_matrix,templist)
            data_matrix=data_transfer(data_matrix)
            filepath='2017datanew/'+str(datas[0])+'.txt'
            with open(filepath,'a') as fileobject:
                for data in data_matrix:
                    fileobject.write(str(data))
                    fileobject.write(',')
                fileobject.write('\n')
            print('Yes')
        print('ok')
main()