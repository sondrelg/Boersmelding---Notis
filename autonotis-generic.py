from sys import argv
import bs4 as bs
from datetime import datetime as dt
import datetime
import requests
import time
import smtplib

class News_scrape():
    
    def __init__(self):
        self.url = 'http://www.netfonds.no/quotes/releases.php?paper=Ticker&days=&location=paper'
        self.time = dt.now()
        self.tickers = []
        self.ticker_dict = {}
    
    def download_tickers(self, exchange='OSE'):
        tickers = []
        resp = requests.get('http://www.netfonds.no/quotes/kurs.php?exchange={}'.format(exchange))            
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class':'mbox'})
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text
            tickers.append(ticker)        
        return(tickers)
                
    def choose_tickers(self):
        oax_tickers = self.download_tickers(exchange='OAX')
        ose_tickers = self.download_tickers(exchange='OSE')
        tickers = []
        print("\nWhat ticker would you like to monitor?")
        while True:
            ticker_input = input('\nEnter "Start" to start.\nTicker: ').upper()
            if ticker_input == "START":
                if len(tickers)>=1: return tickers
                else: print('\n>> No tickers selected. Exiting script.'); exit()                
            print('\n\n\n\n\n\n\n\n\n\n')
            if ((ticker_input in oax_tickers) | (ticker_input in ose_tickers)) & (ticker_input not in tickers): tickers.append(ticker_input)
            elif ticker_input in tickers: print('\n>> Duplicate entry.')
            elif (ticker_input not in oax_tickers) | (ticker_input not in ose_tickers): print('\n>> Ticker not recognized. Please try again.')
            else:  print('>> This isnt meant to happen')
            print("\n\nCurrent selection {}\n".format(tickers))
            print("If you wish to enter more tickers, please do so. To start, type 'start'.")       
        return(tickers)
    
    def scrape_news(self):
        news_messages = []
        for ticker in self.tickers:
            resp = requests.get(self.ticker_dict[ticker])
            soup = bs.BeautifulSoup(resp.text, 'lxml')
            table = soup.find('table', {'class': 'qbox releases'})
            news_messages.append(table.findAll('tr')[1].text)
        return news_messages
    
    def email(self,ticker,news_messages):
        position = self.tickers.index(ticker)
        message = 'NEWS FROM OSLO BØRS!\n'+news_messages[position]
        message = message.encode('iso-8859-1')
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("<e-mail>", "<e-mail password>")
        server.sendmail("<e-mail>", "<e-mail receipient>", message)
        server.quit()
        print(message)
            
    def run(self):
        interval = 30
        if '-i' in argv: print('\n>> Pass "-c" to manually select tickers.\n'); exit()
        if '-t' in argv: 
            try: interval = int(argv[argv.index('-t')+1])
            except: print('\n>> Time input not recognized. Please pass an integer.'); exit()
        if '-c' in argv: self.tickers = self.choose_tickers()
        else:  self.tickers = [<hard coded tickers>]
        for index, entry in enumerate(self.tickers):
            self.ticker_dict[self.tickers[index]] = self.url.replace('Ticker',self.tickers[index])
        print('\n\nMonitoring {} tickers for news; scanning for potential changes once every {} seconds.\n'.format(len(self.tickers),interval))
        benchmark = self.scrape_news()
        while True:
            news_messages = self.scrape_news()
            for index, item in enumerate(news_messages):
                if news_messages[index] != benchmark[index]:
                    self.email(self.tickers[index],news_messages)
                    benchmark[index] = news_messages[index]    
            print("Runtime: {}".format((dt.now()-self.time) - datetime.timedelta(microseconds=(dt.now()-self.time).microseconds)))
            time.sleep(interval)

if __name__ == '__main__':
    News_scrape().run()
