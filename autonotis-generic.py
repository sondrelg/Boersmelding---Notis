import pandas as pd
from bs4 import BeautifulSoup
import bs4 as bs
import datetime as dt
import os
import pandas_datareader.data as web
import pickle
import requests
import lxml
import csv
import requests
import time
import smtplib
urllist = []
tickerlist = []



#Download Tickers Oslo Bors
def bors():
    try:
        resp = requests.get('http://www.netfonds.no/quotes/kurs.php')   ## ACTIVATE THIS FOR OSLO BĂRS                         ## 1
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'mbox'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text
            tickers.append(ticker)             
        with open("ose.pickle","wb") as f:
            pickle.dump(tickers,f)
    except:
        pass
    

#Download Tickers Oslo Axess
def axess():
    try:
        resp = requests.get('http://www.netfonds.no/quotes/kurs.php?exchange=OAX')            
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'mbox'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text
            tickers.append(ticker)        
        with open("axess.pickle","wb") as f:
            pickle.dump(tickers,f)
    except:
        pass


#Create URL's for relevant tickers
def URL_finder_OSE(ticker):
    url1 = "http://www.netfonds.no/quotes/releases.php?paper="
    url2 = "&days=&location=paper&exchange=OSE"
    url_combined = url1+ticker+url2
    urllist.append(url_combined)
def URL_finder_OAX(ticker):
    url1 = "http://www.netfonds.no/quotes/releases.php?paper="
    url2 = "&days=&location=paper&exchange=OSE"
    url_combined = url1+ticker+url2
    urllist.append(url_combined)


#Set up watchlist
def choose_tickers():
    print("What ticker would you like to monitor?")
    df_OSE = pickle.load(open("ose.pickle","rb"))
    df_Axess = pickle.load(open("axess.pickle","rb"))
    y = 2
    while y == 2:
        ticker_add = input("Ticker:")
        ticker_add = ticker_add.upper()
        if ticker_add == "START":
            break
        ticker_exch = input("Please specify 'OAX' or 'OSE' for whether the security is traded on Oslo Axcess or Oslo Børs")
        ticker_exch = ticker_exch.upper()
        
        
        if ticker_exch == "OSE":
            for i in df_OSE:
                if i == ticker_add:
                    tickerlist.append(i)
                    URL_finder_OSE(i)

        else:
            if ticker_exch == "OAX":
                for i in df_Axess:
                    if i == ticker_add:
                        tickerlist.append(i)
                        URL_finder_OAX(i)
            else:
                print("""
                
                Input not recognized. Please try again.
                
                """)
        print("""Your current selection of tickers consists of
        """)
        print(tickerlist)
        print("""
        If you wish to enter more tickers, please do so; otherwise type 'start'""")





#Save news to long-variable
def nyhet_lang():
    yx = []
    for varname in urllist:
        resp = requests.get(varname)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'qbox releases'})
        y = table.findAll('tr')[1].text
        
        yx.append(y)
        with open("nyhet.pickle","wb") as f:
            pickle.dump(yx,f)


#Save news to Short-variable
def nyhet_kort():
    yz = []
    for varname in urllist:
        resp = requests.get(varname)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'qbox releases'})
        z = table.findAll('tr')[1].text
        
        yz.append(z)
        with open("nyhet2.pickle","wb") as f:
            pickle.dump(yz,f)

def email(ticker):
    #Load News
    df = pickle.load(open("nyhet2.pickle","rb"))
    #Transform to string
    msg = df[ticker]
    #Transform to list
    msg = list(msg)
    msg2 = """Nyheter fra oslobors!
    
    """
    #Remove Norwegian letters from text, and recombine to string
    charlist = ['é','í','û','ü','ö','ë','í','é','á','ú','ï']
    for i in msg: 
        if i == "ø":
            i = "o"
            msg2 += i
        else:
            if i == "æ":
                i = "ae"
                msg2 += i
            else:
                if i == "å":
                    i = "aa"
                    msg2 += i
                else:
                    for x in charlist:
                        if x == i:
                            i = ""
                    msg2 += i  
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("YOUR EMAIL ADDRESS HERE", "EMAIL PASSWORD")
    server.sendmail("YOUR EMAIL ADDRESS HERE", "RECEIVING EMAIL ADDRESS HERE", msg2)
    print("MAIL SENT")
    server.quit()



def main():
    
    tid = 0
    bors()
    axess()
    choose_tickers()
    nyhet_lang()
    
    
    ####################################
    df_init = pickle.load(open("nyhet.pickle","rb"))
    print("""
    
    
    
    CURRENT NEWS:
        """)
    for i in df_init:
        print(i)
    print("""
    
    """)
    print(tickerlist)
    ########################################
    
    
    while True:
        nyhet_kort()
        df1 = pickle.load(open("nyhet.pickle","rb"))        
        shortlist = []
        shortcounter = 0
        for i in df1:
            shortlist.append(i)
            shortcounter+=1
        ############################################
        df2 = pickle.load(open("nyhet2.pickle","rb"))    
        longlist = []
        for i in df2:
            longlist.append(i)

        

        if df1 != df2:
            for i in range(0,shortcounter):
                if shortlist[i] != longlist[i]:
                    email(i)
            nyhet_lang()
            time.sleep(60)
    
        else:
            tid+=1
            print("Runtime: %i minute." % tid)
            time.sleep(60)
            

main()

