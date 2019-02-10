import requests
from bs4 import BeautifulSoup
import pandas

base_url = "https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

r=requests.get("https://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c=r.content

soup=BeautifulSoup(c, "html.parser")


page_nbr=soup.find_all("a", {"class": "Page"})[-1].text         #choose the last page to put in "for" loop for changing pages
# print(page_nbr)


list=[]                    #make a list, where we put our stuff (in type of dictionary)


for page in range(0, int(page_nbr)*10, 10):     #we must go through all pages
    url=(base_url+str(page)+".html")
    # print(url)

    r=requests.get(url)
    c=r.content

    soup = BeautifulSoup(c, "html.parser")

    all = soup.find_all("div", {"class": "propertyRow"})   #we choose all divs with properties

    for item in all:                      #in every property we choose some items
        dict={}
        
        dict["Adresses"]=item.find_all("span", {"class": "propAddressCollapse"})[0].text  #this way we choose every item we need
        dict["Locality"]=item.find_all("span", {"class": "propAddressCollapse"})[1].text
        dict["Price"]=item.find("h4", {"class": "propPrice"}).text.replace("\n", "")

        try:                                                                          #use "try" because some items are not exists
            dict["Bed"]=item.find("span", {"class": "infoBed"}).find("b").text
        except:
            dict["Bed"]=None

        try:
            dict["Area"]=item.find("span", {"class": "infoSqFt"}).find("b").text
        except:
            dict["Area"]=None

        try:
            dict["Full Bath"]=item.find("span", {"class": "infoValueFullBath"}).find("b").text
        except:
            dict["Full Bath"]=None

        try:
            dict["Half Bath"]=item.find("span", {"class": "infoValueHalfBath"}).find("b").text
        except:
            dict["Half Bath"]=None
    
        for column_group in item.find_all("div", {"class": "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class": "featureGroup"}), column_group.find_all("span", {"class": "featureName"})):
                if "Lot Size" in feature_group.text:
                    dict["Lot Size"]=feature_name.text

        list.append(dict)     #every dict must be as element in list


df=pandas.DataFrame(list)             #make a good view of stuff
# print(df)

writer = pandas.ExcelWriter('output.xlsx', engine='xlsxwriter')       #this and next rows maked for creating a xlsx file
df.to_excel(writer, sheet_name='Sheet1')
writer.save()
