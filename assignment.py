import bonobo
import requests
from bs4 import BeautifulSoup
import pandas
import json
import csv
from requests_html import HTMLSession
import mysql.connector
from mysql.connector import Error

dictionary={"title":[],"company":[],"location":[]}

def getdata():
    URL = 'https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia'
    session = HTMLSession()
    response = session.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find(id='ResultsContainer') ##finds by id 
    job_elems = results.find_all('section', class_='card-content')
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('div', class_='company')
        location_elem = job_elem.find('div', class_='location')
        if None in (title_elem, company_elem, location_elem):
            continue
        dictionary["title"].append(title_elem.text.strip())
        dictionary["company"].append(company_elem.text.strip())
        dictionary["location"].append(location_elem.text.strip())
    return(dictionary)
        
def fetchdata():
    # fetching data from other source
    URL = 'https://www.indeed.com/q-USA-jobs.html'
    session = HTMLSession()
    response = session.get(URL,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find(id='resultsCol') ##finds by id 
    job_elems = results.find_all('div',class_='jobsearch-SerpJobCard unifiedRow row result')
    for job_elem in job_elems:
        title_elem = job_elem.find('h2', class_='title')
        company_elem = job_elem.find('span', class_='company')
        location_elem = job_elem.find('span', class_='location accessible-contrast-color-location')
        if None in (title_elem, company_elem, location_elem):
            continue
        dictionary["title"].append(title_elem.text.strip())
        dictionary["company"].append(company_elem.text.strip())
        dictionary["location"].append(location_elem.text.strip())
    return(dictionary)

def getdatafromjson():
    f=open("file.json")
    data=json.load(f)
    for datas in data:
        dictionary["title"].append(datas["title"])
        dictionary["company"].append(datas["company"])
        dictionary["location"].append(datas["location"])
    return dictionary

def getdatafromcsv():
    with open("dummy.csv","r",newline="") as file:
        reader=csv.reader(file)
        list_of_column_names=next(reader) 
        for data in reader:
            dictionary["title"].append(data[0])
            dictionary["company"].append(data[1])
            dictionary["location"].append(data[2])
    return dictionary
def getdatafromdatabase():
    try:
        connection = mysql.connector.connect(host='localhost',database='assignment',user='root',password='')
        sql_select_Query = "select * from tbal_data"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print(len(records))
        # count the length of the data fetched and only append it to variable until the data is null
        for record in records:
            dictionary["title"].append(record[0])
            dictionary["company"].append(record[2])
            dictionary["location"].append(record[3])
        return dictionary
    except:
        print("Exception occoured")

def extract():
    yield getdata()
    yield fetchdata()
    yield getdatafromjson()
    yield getdatafromcsv()
    yield getdatafromdatabase()


def transform(*args):
    """Placeholder, change, rename, remove... """
    return args


def load(*args):
    """Placeholder, change, rename, remove... """
    df = pandas.DataFrame(data={"Title":args[0]["title"],"Company":args[0]["company"],"Location":args[0]["location"]})
    df.to_csv("data.csv", sep=',',index=False)


def get_graph(**options):
    """
    This function builds the graph that needs to be executed.
    :return: bonobo.Graph

    """
    graph = bonobo.Graph()
    graph.add_chain(extract, transform, load)

    return graph


def get_services(**options):
    """
    This function builds the services dictionary, which is a simple dict of names-to-implementation used by bonobo
    for runtime injection.

    It will be used on top of the defaults provided by bonobo (fs, http, ...). You can override those defaults, or just
    let the framework define them. You can also define your own services and naming is up to you.

    :return: dict
    """
    return {}


# The __main__ block actually execute the graph.
if __name__ == '__main__':
    headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(
            get_graph(**options),
            services=get_services(**options)
        )