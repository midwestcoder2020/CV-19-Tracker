
import pandas as pd
import folium
from bs4 import BeautifulSoup as bs
import urllib.request
import schedule
import time
import _thread

#folium map
from folium.plugins import MarkerCluster

m =None

def getLatestData():
    url="https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
    content = urllib.request.urlopen(url).read()
    soup = bs(content,features="html.parser")
    links =[]
    for u in soup.find_all('a'):
        if "csv" in u.get('href'):
            #print(u.get('href'))
            links.append(str(u.get('href')))

    fLink = "https://raw.githubusercontent.com"+links[len(links)-1]
    return fLink


def loadData(d):

    data = pd.read_csv(d)
    #data = pd.read_csv("cvdata.csv", delimiter=",")

    return data[['Lat','Long_','Confirmed','Deaths','Recovered','Active','Combined_Key']]

def updateData():

    print("Getting Latest Data")
    data = getLatestData()

    data = data.replace("/blob","")
    #print(data)

    print("Parsing data with Pandas")
    nData = loadData(data)

    print("Creating Map Markers")
    for a in nData.iterrows():

        if  str(a[1]['Lat']) !="nan" and str(a[1]['Long_'] !="nan"):

            folium.CircleMarker([a[1]['Lat'], a[1]['Long_']],radius=20,
                               popup="<h4>"+a[1]['Combined_Key']+"<br>"+"Confirmed Cases: "+str(a[1]['Confirmed'])+" Deaths: "+str(a[1]['Deaths'])+" Recoveries: "+str(a[1]['Recovered'])+"</h4>",
                               tooltip="Click to see stats",
                               color='red',
                               fill=True,
                               fill_color='red'
                               ).add_to(mc)

    print("Updated and saving map")
    m.save('index.html')



def updateThread():
        schedule.run_pending()



if __name__ == '__main__':

    m = folium.Map(location=[45.5236, -122.6750])
    mc = MarkerCluster().add_to(m)
    m.add_child(mc)
    updateData()

    print("creating schedule")
    schedule.every(2).minutes.do(updateData)
    print("schedule created")


    count =0

    while True:
        schedule.run_pending()
        time.sleep(1)

        count +=1

        if count % 10 == 0:
            print("waiting until scheduled task")






    





