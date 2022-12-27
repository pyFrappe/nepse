# NEPSE
## _The Last Nepse Module You'll Ever Need_

Nepse is a realtime nepse scraper which communicates with newweb.nepalstock.com.np, to fetch and return required stats.

#### NOTE :
Nepse's API is not really stable even though it provides realtime information . There is a very reliable and stable api alternative you may wish to try https://kitta.dev/. I will add two sources including nepse's and kitta's on this module soon . Thankyou for using it ! Discord : https://discord.gg/Pdu9D3DMX4

## Features

- Get Brokers
- Get Realtime Prices
- Make Charts and Many More



## Installation

Nepse requires [python3 and pip](http://python.org/) to install and run.

```sh
pip install nepse
```


## Plugins

Nepse is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | LINK |
| ------ | ------ |
| Matplotlib | https://matplotlib.org/|
| Requests | https://pypi.org/project/requests/ |
| Pandas (For Next Update) | https://pandas.pydata.org/ |

## Usage


```py
from nepse import NEPSE
init = NEPSE()

#GET ALL REGISTERED BROKERS
brokers = init.brokers()

#GET ALL NEWS & ALERTS Published By NEPSE on Newweb
news= init.alerts()

#Check IF MARKET IS OPEN
isOpen = init.isOpen() #Returns TRUE IF market is open

#Check live price of specific scrip or get all prices 
allPrices = init.todayPrice()
cghPrice = init.todayPrice('CGH') #returns information for CGH

#CHARTS
chartHistory = init.getChartHistory('CGH') #Get History Prices for CGH
chartHistoryButFiltered = init.getChartHistory('CGH',start_date='2021-03-04',end_date='2021-03-07')

makeChart= init.createChart('CGH',theme='dark',high=False,low=False)#returns abspath of chart saved

csv = init.saveCSV('CGH',start_date='2021-02-07')#filename,start_date and  end_date are optional


indices = init.indices(sector='NEPSE Index',start_date='2021-03-04',end_date='2021-03-07')

floorsheets = init.floorsheets()

#CHECK IPO
result = init.checkIPO(scrip,boid)
{'success': False, 'message': 'Sorry, not alloted for the entered BOID. ', 'body': None}



```


## License

MIT

