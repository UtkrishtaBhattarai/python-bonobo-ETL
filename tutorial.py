import bonobo
import json
import requests
import urllib.request
import pandas


def getdata1():
    name=[]
    f=open("d.json")
    data=json.load(f)
    for x in data:
        name.append(x["name"])
    return name

def getotherdata():
    name2=[]
    url="https://jsonplaceholder.typicode.com/users"
    data=requests.get(url).json()
    for y in data:
        name2.append(y["name"])
    return name2

def getemails():
    emails=[]
    url="https://jsonplaceholder.typicode.com/users"
    data=requests.get(url).json()
    for z in data[0:10]:
        emails.append(z["email"])
    return emails

def getphonenumber():
    phone=[]
    url="https://byrontosh.github.io/landingpage/"
    data=requests.get(url).json()
    for z in data[0:10]:
        phone.append(z["phone"])
    return phone

def getaddress():
    salary=[]
    url="http://dummy.restapiexample.com/api/v1/employees"
    address=requests.get(url).json()
    for sal in address["data"][0:10]:
        salary.append(sal["employee_salary"])
    return salary
    

def extract():
    """Placeholder, change, rename, remove... """
    yield getdata1(),getotherdata(),getemails(),getphonenumber(),getaddress()


def transform(*args):
    # modifying data
    return args[0],args[1],args[2],args[3],args[4]


def load(*args):
    """Placeholder, change, rename, remove... """
    df = pandas.DataFrame(data={"Names": args[0],"Othernames":args[1],"email":args[2],"number":args[3],"salary":args[4]})
    df.to_csv("data.csv", sep=',',index=False)
    df.to_json("data.json",indent=4)
    df.to_html("users.html")
        

def get_graph(**options):
    graph = bonobo.Graph()
    graph.add_chain(
    getotherdata,
    bonobo.Limit(10),
    bonobo.PrettyPrinter(),
    )
    return graph


if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://google.com'
    }
    # scrape_redfin()
    graph = bonobo.Graph(
        extract,
        transform,
        load,
    )
    bonobo.run(graph)