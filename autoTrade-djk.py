import time
from influxdb import InfluxDBClient
import pyupbit


host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'swc'

access = "AT7HeOx48ZzzRDTO5y6FA2Lmw12ufGHwWArU5xVz"
secret = "b4Qg0uZaapuTk18Q7qESC4AQIVboTI9HAhduY4SD"
rows = []
upbit = pyupbit.Upbit(access, secret)

def sell10():
    bal = upbit.get_balances()
    rows = []
    for cfs in bal:
        print(cfs)
        if cfs["currency"]=="KRW":
            pass
        else:
            cnt = float(cfs["balance"])
            if cnt == 0.0:
                pass
            else:
                print(cnt)
                tprice = int(float(cfs["avg_buy_price"])*1.003)
                if tprice > 2000000:
                    tprice = round(tprice/1000)*1000
                elif tprice <= 2000000 and tprice > 1000000:
                    tprice = (round(tprice/1000)*1000)+500
                elif tprice <=1000000 and tprice > 500000:
                    tprice = round(tprice/100)*100
                elif tprice <=500000 and tprice > 100000:
                    tprice = (round(tprice/100)*100)+50
                elif tprice <=100000 and tprice > 10000:
                    tprice = round(tprice/10)*10
                elif tprice <=10000 and tprice > 1000:
                    tprice = (round(tprice/10)*10)+5
                elif tprice <=1000 and tprice > 100:
                    tprice = tprice+round(tprice*0.001,1)
                elif tprice <=100 and tprice >10:
                    tprice = round(float(cfs["avg_buy_price"])*1.002,1)
                else:
                    tprice = round(float(cfs["avg_buy_price"])*1.002,2)
                print(tprice)
                token = "KRW-"+cfs["currency"]
                print(token)
                sret = upbit.sell_limit_order(token,tprice,cnt)
                print(sret)
                rows = rows+list(sret)
    return rows;

def buy10():
    access = "AT7HeOx48ZzzRDTO5y6FA2Lmw12ufGHwWArU5xVz"
    secret = "b4Qg0uZaapuTk18Q7qESC4AQIVboTI9HAhduY4SD"
    upbit = pyupbit.Upbit(access, secret)
    row = None
    client = None
    coins = []
    rows = []
    orders = []
    coinlist = pyupbit.get_tickers()
    client = InfluxDBClient(host, port, user, password, dbname)
    cnt = 0
    for coin in coinlist:
        if coin.startswith("KRW"):
            cnt = cnt +1
        else:
            pass
    sql = "SELECT * FROM CoinRank order by time desc limit "+ str(cnt) +" tz('Asia/Seoul')"
    row = list(client.query(sql))
    row = row[0]
    rows = sorted(row, key=lambda row: (-row['Score']))
    client.close()
    rows = rows[0:5]
    for trade in rows:
        price = trade["Price"]
        if price < 100:
            pass
        else:
            coin = trade["COIN"]
            ret = upbit.buy_market_order(coin,20000)
    return orders;

while True:
    buy10()
    time.sleep(30)
    sell10()
    time.sleep(900)
