from functools import wraps
from datetime import datetime
import pytz
from nepse import NEPSE
from fcache.cache import FileCache
import requests
mycache = FileCache('nepse')



def cachess(func):
    """ 
    This is a decorator function to manage caching for the api requests.
    If the last fetch was done after the 3 PM , then it will ignore new requests
    and provide cached data.

    Also incase of server down it will try to resend request for 3 times and if it fails consecutively 
    the function will look for cached data or will raise an server down exception if it wasn't cached previously.

    """
    @wraps(func)
    def wrap(*args, **kwargs):
        key = f'{(func.__name__)}+@{str(*args)}+@{str(**kwargs)}'
        if key in mycache:
            
            if mycache[key]['fetchHour'] >=15:
                
                return mycache[key]['data']
        tried=0
        while 1:
            try:
                tz = pytz.timezone('Asia/Kathmandu')
                nepal_now = datetime.now(tz)
                current_hour = nepal_now.hour
                data= func(*args, **kwargs)
                
                mycache[key] = {'data':data,'fetchHour':current_hour,'fetchDay':nepal_now.date()}
                mycache.sync()
                return data

                
            except Exception as e:
                print(e)
                if tried >=3:
                    if key in mycache:
                        return mycache[key]['data']
                    raise Exception('Nepse Server Down!')
                tried+=1
                pass
        return func(*args, **kwargs)
    return wrap

@cachess
def marketOpen():
    tz = pytz.timezone('Asia/Kathmandu')
    nepal_now = datetime.now(tz)
    current_hour = nepal_now.hour
    today = nepal_now.strftime('%A')
    if current_hour <=15 and current_hour >=10 and today!='Saturday' and today!='Friday':
        return True
    return False



def todayPrice():
    headers = {
        'authority': 'newweb.nepalstock.com.np',
        'sec-ch-ua': '^\\^',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'origin': 'https://newweb.nepalstock.com.np',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://newweb.nepalstock.com.np/today-price',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = {'id':17}
    
    response = requests.post('https://newweb.nepalstock.com.np/api/nots/nepse-data/today-price', headers=headers, json=data)
    if not response.json():
        _id=requests.get('https://newweb.nepalstock.com.np/api/nots/nepse-data/market-open').json()['id']
        data = ID_MAPPING[_id]
    response = requests.post('https://newweb.nepalstock.com.np/api/nots/nepse-data/today-price', headers=headers, json=data)
    print(response.json())






if __name__ =='__main__':
    print(todayPrice())