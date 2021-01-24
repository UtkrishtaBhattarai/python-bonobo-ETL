import csv
import mysql.connector
from mysql.connector import Error

# import json
# from requests_html import HTMLSession
# import requests
# from bs4 import BeautifulSoup
# dictionary={"title":[],"company":[],"location":[]}

#     # fetching data from other source
# URL = 'https://www.indeed.com/q-USA-jobs.html'
# session = HTMLSession()
# response = session.get(URL)
# soup = BeautifulSoup(response.content, 'html.parser')
# results = soup.find("td",id='resultsCol') ##finds by id 
# print(results)
# exit()
# job_elems = results.find_all('div',class_='jobsearch-SerpJobCard unifiedRow row result')
# for job_elem in job_elems:
#     title_elem = job_elem.find('h2', class_='title')
#     company_elem = job_elem.find('span', class_='company')
#     location_elem = job_elem.find('span', class_='location accessible-contrast-color-location')
#     if None in (title_elem, company_elem, location_elem):
#         continue
#     dictionary["title"].append(title_elem.text.strip())
#     dictionary["company"].append(company_elem.text.strip())
#     dictionary["location"].append(location_elem.text.strip())
# print(dictionary)


# def getdatafromcsv():
#     f=open("file.json")
#     data=json.load(f)
#     print((data))
#     for datas in data:
#         print(datas["company"])
    
# getdatafromcsv()


# def getdatafromcsv():
#     with open("dummy.csv","r",newline="") as file:
#         reader=csv.reader(file)
#         list_of_column_names=next(reader) 
#         for data in reader:
#             print(data)
        
# getdatafromcsv()


try:
    connection = mysql.connector.connect(host='localhost',database='assignment',user='root',password='')
    sql_select_Query = "select * from tbal_data"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    for record in records:
        print(record[0])
    
except:
    print("Exception occoured")