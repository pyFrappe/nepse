import requests
import matplotlib.pyplot as plt
import time
import os
class NEPSE:

    def __init__(self):
        self.headers= {
            'authority': 'newweb.nepalstock.com.np',
            'sec-ch-ua': '^\\^Google',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://newweb.nepalstock.com.np/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        self.host = 'https://newweb.nepalstock.com.np/api/'
        self.securities = requests.get(self.host+'nots/securityDailyTradeStat/58',headers=self.headers).json()
        pass


    def isOpen(self):
        """
        Returns True if the market is Open .

        """
        response = requests.get(self.host+'/nots/nepse-data/market-open', headers=self.headers).json()
        if response['isOpen'] !='CLOSE':
            return True
        return False
    
    def brokers(self):
        """ 
        
        Returns all the registered brokers along with tms url and other information
        
        """
        resp = requests.get(self.host+'nots/member?&size=500',headers=self.headers).json()
        return resp
    
    def alerts(self):
        """
        
        returns alerts and news published by 
        
        """
        resp = requests.get(self.host+'nots/news/media/news-and-alerts',headers=self.headers).json()
        return resp
    
    def todayPrice(self,scrip=None):
        """

        Get Live Price of All The Securities in one call or specify

        """
        resp = requests.get(self.host+'nots/nepse-data/today-price?&size=500',headers=self.headers).json()['content']
        if scrip ==None:
            return resp
        return [script for script in resp if script['symbol']==scrip.upper()][0]

    def markCap(self):
        """
        
        Get Market Caps
        
        """
        resp =requests.get(self.host+'nots/nepse-data/marcapbydate/?',headers=self.headers).json()
        return resp

    def getChartHistory(self,scrip,start_date=None,end_date=None):
        """
        
        returns charts data 
        raises Exception if start_date or end_date != working_days (will fix it)

        """
        scripID = [security for security in self.securities if security['symbol']==scrip.upper()][0]['securityId']
        resp = requests.get(self.host+f'nots/market/graphdata/{scripID}',headers=self.headers).json()
        if start_date:
            start_index = next((index for (index, d) in enumerate(resp) if d["businessDate"] == start_date), None)
            resp = resp[start_index:]
        if end_date:
            end_index =next((index for (index, d) in enumerate(resp) if d["businessDate"] == end_date), None)+1
            resp = resp[:end_index]
        return resp
    
    def createChart(self,scrip,theme='dark',start_date=None,end_date=None,close=True,high=True,low=True):

        symbol = scrip.upper()
        if theme.upper()=='DARK':
            plt.style.use(['dark_background'])
        
        data=self.getChartHistory(symbol,start_date,end_date)
        open_price = [d['openPrice'] for d in data]
        x=[d['businessDate'] for d in data]
        high_data= [d['highPrice'] for d in data]
        low_data = [d['lowPrice'] for d in data]
        close_price= [d['closePrice'] for d in data]

        plt.plot(open_price,label='Open Price')
        if close:
            plt.plot(close_price,label="Close Price")
        if high:
            plt.plot(high_data,label="High")
        if low:
            plt.plot(low_data,label="Low")
        
        plt.legend(loc="upper left")

        plt.title(f'{symbol} Prices As of {x[-1]}')

        plt.xlabel(f"Start Date : {x[0]} | END DATE : {x[-1]}\n\nOPEN PRICE : {open_price[-1]}  | ClOSE PRICE : {close_price[-1]} | High : {high_data[-1]} | Low : {low_data[-1]}")
        ax=plt.gcf().autofmt_xdate()
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([])
        filename =f'{symbol}_{str(time.time())}.png'
        data=plt.savefig(filename)
        abspath = os.path.abspath(filename)
        plt.clf()
        return {'file':abspath}



if __name__ =='__main__':
    data= NEPSE()
    print(data.createChart('CGH'))