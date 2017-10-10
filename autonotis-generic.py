import bs4 as bs
import requests
import time
import smtplib

#Download Tickers Oslo Bors
def ticker_dl():
    try:
        resp = requests.get('http://www.netfonds.no/quotes/kurs.php')  
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'mbox'})
        ose_tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text
            ose_tickers.append(ticker)             
    except:
        pass
    try:
        resp = requests.get('http://www.netfonds.no/quotes/kurs.php?exchange=OAX')            
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'mbox'})
        oax_tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text
            oax_tickers.append(ticker)        
    except:
        pass
    return(ose_tickers,oax_tickers)

#Generate URL's for relevant tickers
def URL_finder_OSE(ticker):
    urllist = []
    pre = "http://www.netfonds.no/quotes/releases.php?paper="
    post = "&days=&location=paper&exchange=OSE"
    combined = pre+ticker+post
    urllist.append(combined)
    return urllist
    
def URL_finder_OAX(ticker):
    urllist = []
    pre = "http://www.netfonds.no/quotes/releases.php?paper="
    post = "&days=&location=paper&exchange=OSE"
    url_combined = pre+ticker+post
    urllist.append(url_combined)
    return urllist

#Set up watchlist
def choose_tickers(df_OSE,df_axess):
    urls = []
    tickers = []
    print("\nWhat ticker would you like to monitor?")
    while True:
        ticker_add = input("\nTicker: ").upper()
        #START SEQUENCE
        if ticker_add == "START":
            if len(urls)>=1:
                return urls,tickers
            else:
                print('\nNo tickers selected.')
                exit()                
        #EXCHANGE SELECTION
        print("\nPlease specify 'OAX' or 'OSE' for whether the security is traded on Oslo Axcess or Oslo Bors.")
        ticker_exch = input("\nExchange: ").upper()
        if ticker_exch == "OSE":
            if ticker_add in df_OSE and ticker_add not in tickers:
                urls.append(URL_finder_OSE(ticker_add))       
                tickers.append(ticker_add)
                print("\n\nCurrent selection {}\n".format(tickers))
                print("If you wish to enter more tickers, please do so. To start, type 'start'.")       
            elif ticker_add not in df_OSE:
                print('\nTicker not in Oslo Bors. Try again.')
            else:
                print('\nDuplicate entry.')
        elif ticker_exch == "OAX":
            if ticker_add in df_axess and ticker_add not in tickers:
                urls.append(URL_finder_OAX(ticker_add))
                tickers.append(ticker_add)
                print("\n\nCurrent selection {}\n".format(tickers))
                print("If you wish to enter more tickers, please do so. Otherwise, type 'start'.")       
            elif ticker_add not in df_axess:
                print('\nTicker not in Oslo Axess. Try again.')
            else:
                print('\nDuplicate entry.')
        else:
            print("\nInput not recognized. Please try again.")
    return(urls, tickers)

#Save news to long-cycle variable
def news_dl(urls):
    newslist = []
    for url in urls:
        resp = requests.get(url[0])
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'qbox releases'})
        news = table.findAll('tr')[1].text
        newslist.append(news)
    return(newslist)

#Email package crashes if non-UTF8 characters are included.
def clean_msg(msg):
    charlist = [['é','e'],['í','i'],['û','u'],['ü','u'],['ö','oe'],['ë','e'],['í','i'],['é','e'],['á','a'],['ú','u'],['ï','i'],['ø','oe'],['æ','ae'],['å','aa']]
    for i in charlist:
        msg=msg.replace(i[0],i[1])
    return msg

#FIX INTO DOUBLE-ENTRIED DICT 
def email(msg):
    msg = "Nyheter fra Oslo Bors!\n"+clean_msg(msg)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("YOUR EMAIL ADDRESS HERE", "EMAIL PASSWORD")
    server.sendmail("YOUR EMAIL ADDRESS HERE", "RECEIVING EMAIL ADDRESS HERE", msg)
    print("""-----------------------  MAIL SENT:  --------------------------\n
    {}
    ---------------------------------------------------------------""".format(msg))
    server.quit()

def main():
    tid = time.time()
    ose_tickers=[]
    oax_tickers=[]
    watchlist=[]
    #First we create a local list of viable tickers
    ose_tickers, oax_tickers = ticker_dl()
    #Secondly, we prompt for tickers to monitor - tickers need to exist in the
    #list of viable choices
    urls, watchlist = choose_tickers(ose_tickers,oax_tickers)    
    #Once the watchlist has been defined, we start by logging the 
    #most recent news event for each security, which we will use as a benchmark.
    print("\n\nCURRENT NEWS: \n")
    df1 = news_dl(urls)    
    for i in df1:
        print(clean_msg(i))
        time.sleep(1.5)
    print("Watchlist: {}\n".format(watchlist))
    #Monitor for new news
    while True:
        df2 = news_dl(urls)
        if df1 != df2:
            for i in range(0,len(df1)):
                if df1[i] != df2[i]:
                    email(i)
            df1 = df2
            time.sleep(60)
        else:
            print("Runtime: {} minute(s)".format(round((time.time()-tid)/60)))
            time.sleep(60)
            
if __name__ == '__main__':
    main()
















