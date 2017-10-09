# Boersmelding---Notis
Lets you monitor a selection of Norwegian stocks for news. News events are emailed to the user.

Requirements:
- bs4 (BeautifulSoup)       #For data
- pickle                    
- pandas
- smtplib                   #For email functionality

Oslo Bors provides this exact service by SMS (https://www.oslobors.no/Oslo-Boers/Produkter-og-tjenester/SMS-tjenester/Varslinger-paa-SMS), but if you prefer not to pay for the service, here is a simple way to get more or less the same functionality.

For e-mail functionality enter account details in lines ~165-166.


------------------

This script is configured to prompt you for stocks you're interested in monitoring, but hard-coding your watchlist is simple. I run this on my raspberry pi, and find that hard-coding the watchlist is more convenient.

The script refreshes every 60 seconds to check for news. The frequency can be changed at the very end of the script.
