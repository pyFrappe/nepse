import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime,timedelta
import time
import os
import queue
import threading

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
        #https://github.com/Samrid-Pandit/nepse-api/blob/master/nepse/utils.py#L13
        #Thanks to Saya for quick patch
        self.ID_MAPPING ={

            3: 896,
            5: 167,
            7: 359,
            8: 890,
            11: 318,
            12: 482,
            13: 574,
            14: 895,
            16: 620,
            15: 582,
            17: 345,
            18: 326,
            19: 515,
            23:564,
            24: 662,
            25: 198,
            26:600,
            27: 511,
            28: 469,
            29: 537,
            30: 352,
            31: 407,
            32: 287,
            33: 479,
            34: 613,
        }
        
        self.sectors=[{'id': 51, 'indexCode': 'BANKSUBIND', 'indexName': 'Banking SubIndex', 'description': 'Index of All the Listed Commercial Banks', 'sectorMaster': {'id': 37, 'sectorDescription': 'Commercial Banks', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Rastra Bank'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 76657.9194}, {'id': 52, 'indexCode': 'HOTELIND', 'indexName': 'Hotels And Tourism Index', 'description': 'All the companies Listed in Hotels Group', 'sectorMaster': {'id': 39, 'sectorDescription': 'Hotels and Tourism', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 1604.146}, {'id': 53, 'indexCode': 'OTHERSIND', 'indexName': 'Others Index', 'description': 'All the companies Listed in Others  Group', 'sectorMaster': {'id': 40, 'sectorDescription': 'Others', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 
            16655.8076}, {'id': 54, 'indexCode': 'HYDPOWIND', 'indexName': 'HydroPower Index', 'description': 'All the companies listed in Hydropower Group', 'sectorMaster': {'id': 41, 'sectorDescription': 'Hydro Power', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 11375.7071}, {'id': 55, 'indexCode': 'DEVBANKIND', 'indexName': 'Development Bank Index', 'description': 'Index of  the listed development Banks', 'sectorMaster': {'id': 44, 'sectorDescription': 'Development Banks', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Rastra Bank'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 3717.0987}, {'id': 56, 'indexCode': 'MANPROCIND', 'indexName': 'Manufacturing And Processing', 'description': 'Manufacturing and Processing Index', 'sectorMaster': {'id': 38, 'sectorDescription': 'Manufacturing And Processing', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 2425.7603}, {'id': 57, 'indexCode': 'SENSIND', 'indexName': 'Sensitive Index', 'description': 'Sensitive Index', 'sectorMaster': {'id': 51, 
            'sectorDescription': 'ALL', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 297165.8107}, {'id': 58, 'indexCode': 'NEPSE', 'indexName': 'NEPSE Index', 'description': 'All Equity Index', 'sectorMaster': {'id': 51, 'sectorDescription': 'ALL', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'Y', 'baseYearMarketCapitalization': 138470.1734}, {'id': 59, 'indexCode': 'NONLIFIND', 'indexName': 'Non Life Insurance', 'description': 'All Non Life Insurance Index', 'sectorMaster': {'id': 43, 'sectorDescription': 'Non Life Insurance', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Insurance Board'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 1914.4838}, {'id': 60, 'indexCode': 'FININD', 'indexName': 'Finance Index', 'description': 'Index of Finance Companies', 'sectorMaster': {'id': 45, 'sectorDescription': 'Finance', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Rastra Bank'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 3327.7232}, {'id': 61, 'indexCode': 'TRDIND', 'indexName': 'Trading Index', 'description': 'All Trading Companies', 'sectorMaster': {'id': 42, 'sectorDescription': 'Tradings', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 581.9577}, {'id': 62, 'indexCode': 'FLOATIND', 'indexName': 'Float Index', 'description': 'All Float Index', 'sectorMaster': {'id': 51, 'sectorDescription': 'ALL', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 698600.0336}, {'id': 63, 'indexCode': 'SENSFLTIND', 'indexName': 'Sensitive Float Index', 'description': 'All Sensitive Float Index', 'sectorMaster': {'id': 51, 'sectorDescription': 'ALL', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 308604.0344}, {'id': 64, 'indexCode': 'MICRFININD', 'indexName': 'Microfinance Index', 'description': 'all microfinance company index', 'sectorMaster': {'id': 49, 'sectorDescription': 'Microfinance', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Rastra Bank'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 7133.2871}, {'id': 65, 'indexCode': 'LIFINSIND', 'indexName': 'Life Insurance', 'description': 'All Life Insurance Index', 'sectorMaster': {'id': 50, 'sectorDescription': 'Life Insurance', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Insurance Board'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 2119.7235}, {'id': 66, 'indexCode': 'MUTUALIND', 'indexName': 'Mutual Fund', 
            'description': 'All Mutual Fund Index', 'sectorMaster': {'id': 46, 'sectorDescription': 'Mutual Fund', 'activeStatus': 'A', 'regulatoryBody': 'N/A'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 25704.9716}, {'id': 67, 'indexCode': 'INVIDX', 'indexName': 'Investment Index', 'description': 'All Investment Index', 'sectorMaster': {'id': 52, 'sectorDescription': 'Investment', 'activeStatus': 'A', 'regulatoryBody': 'Nepal Rastra Bank'}, 'activeStatus': 'A', 'keyIndexFlag': 'N', 'baseYearMarketCapitalization': 290499.5699}]
        self.host = 'https://newweb.nepalstock.com.np/api/'
        self.securities = requests.get(self.host+'nots/securityDailyTradeStat/58',headers=self.headers).json()
        pass
    
    def fetchPayload(self):
        _id=requests.get(self.host+'nots/nepse-data/market-open',headers=self.headers).json()['id']
        return self.ID_MAPPING[_id]


    
    def dateFilter(self,working_date,data):
        """
        Function to return next working day , if the date provided is non-working day.

        Returns either first or last date if the date provided is too ahead or too back.

        """

        all_dates =[date['businessDate'] for date in data]
        if working_date in all_dates:
            return working_date
        else:
            i=0
            while 1:

                date=datetime.strptime(working_date,'%Y-%m-%d')
                new_date=str(date+timedelta(days=i)).split(' ')[0]
                if new_date in all_dates:
                    return new_date
                i+=1
                if i>=7:
                    month = working_date.split('-')[1]
                    year =  working_date.split('-')[0]
                    day=working_date.split('-')[-1]
                    if year > all_dates[-1].split('-')[0] and month > all_dates[-1].split('-')[1]:
                        return all_dates[-1]
                    return all_dates[0]
            

    def isOpen(self):
        """
        Returns True if the market is Open .

        """
        response = requests.get(self.host+'/nots/nepse-data/market-open', headers=self.headers).json()
        if response['isOpen'] !='CLOSE':
            return True
        return False
    
    
    def nonthreadedfloorsheets(self):
        content =[]
        page=0
        while 1:
            response = requests.get('https://newweb.nepalstock.com.np/api/nots/nepse-data/floorsheet?page={page}&size=2000&sort=contractId,desc',
            headers=self.headers)
            data=(response.json())['floorsheets']['content']
            isLast = response.json()['floorsheets']['last']
            content.extend(data)
            page+=1
            if isLast:
                return content
    
    def floorsheets(self):
        """
        Threaded Scraper For FloorSheets as we need to scrape more than 75k Data
        Returns in less than 2 seconds.
        """
        q = queue.Queue()
        contents=[]
        response = requests.post(self.host+'nots/nepse-data/floorsheet?size=500&sort=contractId,desc', headers=self.headers,json={'id':198})
        if not response.json():
            data={'id':self.fetchPayload()}
            response = requests.post(self.host+'nots/nepse-data/floorsheet?size=500&sort=contractId,desc', headers=self.headers,json=data)

        pages = response.json()['floorsheets']['totalPages']

        def scrapePage(pageNUM):
            while 1:
                tried=0
                try:
            
                    response = requests.post(self.host+f'nots/nepse-data/floorsheet?page={pageNUM}&size=500&sort=contractId,desc', headers=self.headers,json={'id':198})
                    if not response.json():
                        data={'id':self.fetchPayload()}
                        response = requests.post(self.host+f'nots/nepse-data/floorsheet?page={pageNUM}&size=500&sort=contractId,desc', headers=self.headers,json=data)
                    break
                except Exception:
                    tried+=1
                    if tried>5:
                        raise Exception('NEPSE RATELIMITED')
                    pass
            return response.json()['floorsheets']['content']

        def queGET(q):
            while True:
                task = q.get()
                contents.extend(scrapePage(task))
                q.task_done()

        
        for i in range(30):
            worker = threading.Thread(target=queGET, args=(q,), daemon=True)
            worker.start()

        for j in range(pages):
            q.put(j)

        q.join()

        return contents
    

    def indices(self,sector='NEPSE Index',start_date=None,end_date=None):
        index=sector
        index_id = [id['id'] for id in self.sectors if id['indexName']==index][0]
        resp= requests.get(self.host+f'nots/index/history/{index_id}?size=500',headers=self.headers).json()['content']
        if start_date:
            start_date = self.dateFilter(start_date,resp)
            start_index = next((index for (index, d) in enumerate(resp) if d["businessDate"] == start_date), None)
            resp = resp[start_index:]
        if end_date:
            
            end_date = self.dateFilter(end_date,resp)
            end_index =next((index for (index, d) in enumerate(resp) if d["businessDate"] == end_date), None)+1
            if start_date and end_date:
                if end_index == start_index:
                    end_index =-1
            resp = resp[:end_index]
        return resp


        
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

        resp = requests.get(self.host+'/nots/securityDailyTradeStat/58',headers=self.headers).json()
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
            start_date = self.dateFilter(start_date,resp)
            start_index = next((index for (index, d) in enumerate(resp) if d["businessDate"] == start_date), None)
            resp = resp[start_index:]
        if end_date:
            
            end_date = self.dateFilter(end_date,resp)
            end_index =next((index for (index, d) in enumerate(resp) if d["businessDate"] == end_date), None)+1
            if start_date and end_date:
                if end_index == start_index:
                    end_index =-1
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

    def saveCSV(self,scrip,start_date=None,end_date=None,filename=None):
        resp = self.getChartHistory(scrip,start_date,end_date)
        if not filename:
            filename = f'{scrip.upper()}_{str(time.time())}.csv'
        pd.DataFrame(resp).to_csv(filename)
        return os.path.abspath(filename)
    
    def checkIPO(self,scrip,boid):
        """
        CHECK IPO RESULT

        """

        scripID = [resp['id'] for resp in requests.get('https://iporesult.cdsc.com.np/result/companyShares/fileUploaded').json()['body'] if resp['scrip']==scrip.upper()][0]

        return requests.post(
            'https://iporesult.cdsc.com.np/result/result/check',
            json={"companyShareId":scripID,"boid":boid}).json()

    



if __name__ =='__main__':
    data= NEPSE()
    print(data.todayPrice('CGH'))
