# Boersmelding---Notis
Lets you monitor a selection of Norwegian stocks for news. News events are emailed to the user.

Requirements:
- bs4 (BeautifulSoup)       #For data
- pickle                    
- pandas
- smtplib                   #For email functionality

Oslo Bors provides this exact service by SMS (https://www.oslobors.no/Oslo-Boers/Produkter-og-tjenester/SMS-tjenester/Varslinger-paa-SMS), but if you prefer not to pay for the service, here is a simple way to get more or less the same functionality.

You do need to enter your e-mail details in lines ~165-166.


------------------

This script is configured to ask you which stocks you're interested in monitoring at launch, but pre-defining your watchlist is easily done. I run this on my raspberry pi, and find that pre-configuring the watchlist is more convenient to let it run on startup.

The script refreshes every 60 seconds to check for news. The frequency can be shortened or lengthened by changing the pause at the very end of the script.
