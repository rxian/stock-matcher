import bs4 as bs
import requests

sp_500_companies = []
ticker_company_name_dict = {}

def generate():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
                        headers=headers)

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text.replace("\n", "")
        company = preprocess(row.findAll('td')[1].text)
        sp_500_companies.append(company)
        ticker_company_name_dict[ticker] = company

def preprocess(text):
    text = text.replace("\n", "")

    text = text.replace(" Corp", "")
    text = text.replace(" Corp.", "")
    text = text.replace(" Co", "")
    text = text.replace(" Co.", "")
    text = text.replace(" & Co.", "")
    text = text.replace(" & Co", "")

    text = text.replace(" Corporation", "")

    text = text.replace(" Inc.", "")
    text = text.replace(" ,Inc.", "")
    text = text.replace(" Inc", "")
    text = text.replace(" ,Inc", "")
    
    text = text.replace(" Systems", "")
    text = text.replace(" Brands", "")
    text = text.replace(" Companies", "")
    text = text.replace(" Limited", "")
   
    text = text.replace(" (Class A)", "")
    text = text.replace(" (Class C)", "")
    text = text.replace(".com ", "")
    text = text.replace(" plc", "")
    text = text.replace(" Group", "")

    return text
    