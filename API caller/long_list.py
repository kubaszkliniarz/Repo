import bs4 as bs
import pickle
import requests


def get_tickers():

    ###Funkcja do sciagania tabeli z wikipedii z  tickerami firm z indeksu S&P
    ###Potrzebne zmienne do operacji
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    wiki_table = soup.find('table', {'class': 'wikitable sortable'}) #wyszukanie tabeli ktora znajduje sie w klasie wikitable
    tickers = []
    names=[]
    ###Przechodzimy po kazdym rekordzie w tabeli (posrod <tr> </tr>, nastepnie widzac, ze nasz ticker znajduje sie w pierwszym <td> </td>, tak wiec kazdy rzad tabeli jest wsrod <tr>, a potem kazdy element tej tabeli wsrod <td>

    for row in wiki_table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        # Wyciagniete tickery posiadaja na koncu znak nowej linii badz spacje, tak wiec chce sie ich pozbyc
        ticker = ticker.replace('\n', '').replace(' ','')

        tickers.append(ticker)
        #Analogicznie dla company name
        company_name = row.findAll('td')[1].text

        company_name = company_name.replace('\n', '').replace(' ', '')

        names.append(company_name)

    ###Zwracam jako dictionary, aby w glownym skrypcie poslugiwac sie tickerami (w taki sposob moge jedynie wyszukac notowania w API),
    ###natomiast aby uzytkownikowi wyswietlac pelne nazwy spolek
    return dict(zip(names, tickers))
