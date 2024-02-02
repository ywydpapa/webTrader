import pyupbit
import time
from datetime import datetime
from influxdb import InfluxDBClient
import json
import numpy


envhost = 'localhost'
envuser = 'root'
envpassword = 'root'
envdb = 'swc'
envport = 8086
client = InfluxDBClient(envhost,envport, envuser, envpassword, envdb)

access = "AT7HeOx48ZzzRDTO5y6FA2Lmw12ufGHwWArU5xVz"
secret = "b4Qg0uZaapuTk18Q7qESC4AQIVboTI9HAhduY4SD"
upbit = pyupbit.Upbit(access, secret)
cnt2 = 1
while True:
    coinNames = pyupbit.get_tickers()
    for coinName in coinNames:
        if coinName.startswith("KRW"):
            curprice = pyupbit.get_orderbook(coinName)
            print(coinName)
            timest = curprice['timestamp']
            times = str(timest)
            times = times[0:10]
            timestm = datetime.fromtimestamp(int(times))
            print(timestm)
            totalask = curprice['total_ask_size']
            print(totalask)
            totalbid = curprice['total_bid_size']
            print(totalbid)
            buyrate = totalask / totalbid * 100
            print("BuyRate : ", buyrate)
            if totalbid > totalask:
                mktsts = 'DOWN'
            else:
                mktsts = 'RAISE'
            units = curprice['orderbook_units']
            cnt = 1
            for unit in units:
                measurement = 'CoinStatus'
                askrate = float(unit['ask_size'])/float(totalask)*100
                bidrate = float(unit['bid_size'])/float(totalbid)*100
                tags = {'COIN':coinName, 'TimeStamp': timestm , 'AskAmt':totalask, 'BidAmt': totalbid, 'BuyRate': buyrate, 'MarketStatus': mktsts, 'Serial':cnt}
                fields = {'ask_price':float(unit['ask_price']),'bid_price':float(unit['bid_price']),'ask_size':float(unit['ask_size']),
                          'bid_size':float(unit['bid_size']), 'ask_rate': float(askrate), 'bid_rate':float(bidrate)}
                insdata = [{'measurement': measurement,'tags': tags, 'fields': fields}]
                client.write_points(insdata)
                cnt = cnt+1
            time.sleep(0.5)
        else:
            pass
        print(cnt2)
    cnt2=cnt2+1
