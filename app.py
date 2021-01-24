import bonobo
import requests
from bs4 import BeautifulSoup
import pandas
 
 
def scrape_zillow():
    price = ''
    status = ''
    url = 'https://www.zillow.com/homedetails/41-Norton-Ave-Dallas-PA-18612/2119501298_zpid/'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = r.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        price_status_section = soup.select('photo-cards photo-cards_wow photo-cards_short')
        price(price_status_section)
        if len(price_status_section) > 1:
            price = price_status_section[1].text.strip()
    return price
 
 
def scrape_redfin():
    price = ''
    status = ''
    url = 'https://www.redfin.com/TX/Dallas/2619-Colby-St-75204/unit-B/home/32251730'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        html = r.text.strip()
        soup = BeautifulSoup(html, 'lxml')
        price_section = soup.find('span', {'itemprop': 'price'})
        if price_section:
            price = price_section.text.strip()
    return price
 
 
def extract():
    yield scrape_zillow()
    yield scrape_redfin()
 
 
def transform(price: str):
    t_price = price.replace(',', '').lstrip('$')
    return str(t_price)
 
 
def load(price: str):
    df = pandas.DataFrame(data={"Prices":price})
    df.to_csv("pricing.csv")
 
 
if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'referrer': 'https://google.com'
    }
    # scrape_redfin()
    graph = bonobo.Graph(
        extract,
        transform,
        load,
    )
    bonobo.run(graph)