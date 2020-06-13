import yfinance as yf #Funkcja sluzaca do latwego dostepu do API Yahoo , https://pypi.org/project/yfinance/, https://github.com/ranaroussi/yfinance
from tkinter import *
import matplotlib.pyplot as plt
import long_list #korzystam z drugiego pliku, w ktorym mam funkcje scrapujaca strone wikipedii z aktualnymi spolkami nalezacymi do S&P
from tkinter import ttk
from datetime import date, datetime, timedelta #operacje na 'czasie'
from dateutil.relativedelta import relativedelta #operacje na 'czasie'
import numpy as np
from tkinter.messagebox import showerror
import sys

###Funkcja sterujaca operacjami na danych
def download_history():

    ###z dropdownow zbieram informacje o wybranej dacie, a takze o wybranej spolce
    date1, date2 = date_choice()
    try:
        company_selected = company_names[dropdown.get()]
    except KeyError:
        print("Wybierz jakas spolke!")
        showerror(title="Error!", message="Wybierz jakas spolke!")
    print("Wybrano spolke: ", company_selected)

    #print(yf.download(company_selected, start=date2, end=date1))
    ###Pobieranie danych z yfinance
    data=(yf.download(company_selected, start=date2, end=date1))
    ###Przejscie do funkcji, ktora liczy nam statystyki
    calculations(data)
    #graph(data, company_selected)

###Funkcja wywolywana za pomoca przycisku "Wykres" (Button2), ktora nasze dane obrazuje w formie graficznej
def graph():

    date1, date2 = date_choice()
    try:
        company_selected = company_names[dropdown.get()]
    except KeyError:
        print("Wybierz jakas spolke!")
        showerror(title="Error!", message="Wybierz jakas spolke!")
    data = (yf.download(company_selected, start=date2, end=date1)) ##To do usuniecia jesli nie dziala
    #print(data['Adj Close'])

    ###Ustalamy nasza figure i jej wielkosc
    fig=plt.figure(figsize=(6, 15))
    ###Tworze pierwszy 'subplot'. Korzystam z subplotow, aby wykresy byly  ustawione wertykalnie, ze wspolna osia X.  Dzieki temu mozemy porywnac relacje wolumenu do np. duzego spadku
    ax1=plt.subplot(211)
    ax1.plot(data['Adj Close'])
    ###Ustawiam pod katem 45st. axis na osi X, aby daty nie nachodzily na siebie i byly czytelne
    plt.xticks(rotation=45)
    plt.ylabel("Wartosc zamkniecia w danym dniu")
    plt.title('Notowania spolki '+ company_selected + ' w wybranym okresie')

    ax2=plt.subplot(212, sharex=ax1)
    ax2.plot(data['Volume']/1000)
    plt.xticks(rotation=45)
    plt.ylabel("Wolumen (000)")
    plt.title('Wolumen w wybranym okresie')
    plt.show()

###Funkcja zwracajaca daty poczatku i konca okresu, ktory chcemy analizowac
def date_choice():
    if dropdown_date.get() == '1 tydzien':
        return today_string, (today - relativedelta(weeks=1)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '2 tygodnie':
        return today_string, (today - relativedelta(weeks=2)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '1 miesiac':
        return today_string, (today - relativedelta(months=1)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '2 miesiace':
        return today_string, (today - relativedelta(months=2)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '3 miesiace':
        return today_string, (today - relativedelta(months=3)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '6 miesiecy':
        return today_string, (today - relativedelta(months=6)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '9 miesiecy':
        return today_string, (today - relativedelta(months=9)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '12 miesiecy':
        return today_string, (today - relativedelta(months=12)).strftime("%Y-%m-%d")
    elif dropdown_date.get() == '24 miesiace':
        return today_string, (today - relativedelta(months=24)).strftime("%Y-%m-%d")
    else:
        showerror(title="Error!", message="Wybierz jakis okres czasu!")
        print("Issue with date_choice function.")
        sys.exit(1)


##Funkcja liczaca nasze statystyki
def calculations(data):
    average_volume = round(data['Volume'].mean(), 3)
    #print("Srednia wolumenu: ", average_volume)
    average_close = round(data['Adj Close'].mean(), 3)
    #print("Srednia notowan: ", average_close)
    perc_change = round(((data['Adj Close'].tail(1).values[0] / data['Adj Close'].head(1).values[0]) - 1), 5)
    perc_change2 = (f"{perc_change:.0%}")
    #print(perc_change2)
    #print(data)
    max = round(data['Adj Close'].max(skipna=True), 2)
    row_max = data['Adj Close'].idxmax()
    min = round(data['Adj Close'].min(skipna=True), 2)
    row_min = data['Adj Close'].idxmin()
    max_v = round(data['Volume'].max(skipna=True), 2)
    row_max_v = data['Volume'].idxmax()
    min_v = round(data['Volume'].min(skipna=True), 2)
    row_min_v = data['Volume'].idxmin()
    #print(min, " ", row_min)
    #print(max, " ", row_max)
    standard_deviation = round(data['Adj Close'].std(), 3)
    #print(standard_deviation)
    global calculations_text

    ###Wyswietlenie naszych statystyk na oknie Tkintera
    calculations_text = Label(text="Srednia notowan wynosi: " + str(average_close) +
                                "\nSrednia wolumenu wynosi: " + str(average_volume) +
                                "\nZmiana procentowa notowania wynosi: " + str(perc_change2) +
                                "\nMaksymalna wartosc notowan dla "+ str(row_max)[:10] + " wynosi: " + str(max) + ###[:10], ze wzgledu na format daty YYYY-MM-DD HH-MM-SS, chcemy sama date, bez godzin.
                                "\nMinimalna wartosc notowan dla " + str(row_min)[:10] + " wynosi: " + str(min) +
                                "\nMaksymalna wartosc wolumenu dla "+ str(row_max_v)[:10] + " wynosi: " + str(max_v) +
                                "\nMinimalna wartosc wolumenu dla " + str(row_min_v)[:10] + " wynosi: " + str(min_v) +
                                "\nOdchylenie standardowe notowan wynosi: " + str(standard_deviation))
    calculations_text.pack()

###########################################################################################################

today = date.today()
today_string = today.strftime("%Y-%m-%d")

###Podstawowe komendy charakteryzujaca nasze okno Tkintera
root = Tk()
root.geometry("600x600")
root.title('API Caller for S&P stocks')

###Pierwszy napis
header_text = Label(root, text="Wybierz z listy spolke:")
header_text.pack()

#clicked = StringVar()

###Wywolanie naszej funkcji z pliku long_list.py, ktora przekazuje nam tickery spolek S&P
company_names = long_list.get_tickers()

#dropdown = OptionMenu(root, clicked, *company_names.keys())
#dropdown = Spinbox(root, values=list(company_names), textvariable=clicked, command=download_history)

###Skorzystalem z Comboboxa, z pakietu ttk pod Tkinterem, ze wzgledu na jego scrollbar po prawej stronie, ktorego nie ma w OptionMenu
dropdown = ttk.Combobox(root, state="readonly", values=list(company_names))
dropdown.pack()

list_of_dates = [
    '1 tydzien',
    '2 tygodnie',
    '1 miesiac',
    '2 miesiace',
    '3 miesiace',
    '6 miesiecy',
    '9 miesiecy',
    '12 miesiecy',
    '24 miesiace'
]

dropdown_date = ttk.Combobox(root, state="readonly", values=list_of_dates)
dropdown_date.set('2 tygodnie')
period_text = Label(root, text="Wybierz okres notowan spolki:")
period_text.pack()
dropdown_date.pack()

Button1 = Button(root, text="Obliczenia", command=download_history).pack()
Button2 = Button(root, text="Wykres", command=graph).pack()
Button3 = Button(root, text="Skasuj ostatnia statystyke", command=lambda: calculations_text.destroy()).pack() ###Przycisk do usuwania ostatnio wyswietlonych statystyk



root.mainloop()


# if __name__=="__main__":
#     main()