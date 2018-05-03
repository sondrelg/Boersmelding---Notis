# Børsmelding - Notis
Lets you monitor a selection of Norwegian stocks for news. News events are emailed to the user. Oslo Bors also provides this exact service by SMS (https://www.oslobors.no/Oslo-Boers/Produkter-og-tjenester/SMS-tjenester/Varslinger-paa-SMS).

### Required modules:
- bs4
- smtplib
- datetime

### Before running
Before running, any user will need to:
- Enter e-mail account details in lines 61-62 for e-mail functionality.
- Hard code stock tickers in line 73. 

### Notes
While the script is configured to monitor the hard-coded Norwegian stocks defined in the script, some simple optionalities have been added for ease of use:

- To manually enter tickers for monitoring, pass "-c" when running.
- To alter the frequency news are checked (default: 30 sec), pass "-t <seconds>".

Example: "python Notis.py -c -t 120"
