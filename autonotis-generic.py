import bs4 as bs
import pickle
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

#Generate URL's for relevant tickers
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
    print("What ticker would you like to monitor?".encode('utf-8'))
    df_OSE = pickle.load(open("ose.pickle","rb"))
    df_Axess = pickle.load(open("axess.pickle","rb"))
    y = 2
    while y == 2:
        ticker_add = input("Ticker: ")
        ticker_add = ticker_add.upper()
        if ticker_add == "START":
            break
        print("Please specify 'OAX' or 'OSE' for whether the security is traded on Oslo Axcess or Oslo Bors.".encode('utf-8'))
        ticker_exch = input("Exchange: ".encode('utf-8'))
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
                print("Input not recognized. Please try again.".encode('utf-8'))
        print("Your current selection of tickers consists of{}If you wish to enter more tickers, please do so; otherwise type 'start'".format(tickerlist).encode('utf-8'))

#Save news to long-cycle variable
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

#Save news to Short- cyclevariable
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
    msg2 = "Nyheter fra oslobors!"
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
    tid = time.time()
    #Download Tickers from OSE (Exchange)  
    bors()
    #Download Tickers from OAX (Exchange)
    axess()
    #Get tickerlist
    choose_tickers()
    #Store current news in pickle
    nyhet_lang()
    #Retrieve current news
    df_init = pickle.load(open("nyhet.pickle","rb"))
    #Print current news
    print("CURRENT NEWS: ")
    for i in df_init:
        print("Watchlist: {}".format(i).encode('utf-8'))
    print(tickerlist)
    #Monitoring for new news
    while True:
        nyhet_kort()
        df1 = pickle.load(open("nyhet.pickle","rb"))        
        shortlist = []
        shortcounter = 0
        for i in df1:
            shortlist.append(i)
            shortcounter+=1
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
            print("Runtime: {} minute(s)".format(round((time.time()-tid)/60)))
            time.sleep(60)
            
if __name__ == '__main__':
    main()
