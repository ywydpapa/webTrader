import pymysql as my
from influxdb import InfluxDBClient
import pyupbit
import os
from dotenv import load_dotenv

load_dotenv()
envhost = os.getenv('envhost')
envuser = os.getenv('envuser')
envpassword = os.getenv('envpassword')
envdb = os.getenv('envdb')
envcharset = os.getenv('envcharset')

host = 'swc9004.iptime.org'
port = 8086
user = 'root'
password = 'root'
dbname = 'swc'

def selectUsers(uid, upw):
    row = None
    connection = None
    try:
        connection = my.connect(host=envhost,
                                user=envuser,
                                password=envpassword,
                                database=envdb,
                                cursorclass=my.cursors.DictCursor
                                )
        cursor = connection.cursor()
        sql = '''SELECT * FROM userAccount WHERE userId=%s AND userPasswd=password(%s)'''
        cursor.execute(sql, (uid, upw))
        row = cursor.fetchone()
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:
            connection.close()
    return row

def coinStat60(coinname):
    rows = None
    client = None
    client = InfluxDBClient(host, port, user, password, dbname)
    sql = "SELECT * FROM CoinStatus where Serial = '1' and COIN = "+"'"+coinname+"'"+" order by time desc limit 60 tz('Asia/Seoul')"
    rows = client.query(sql)
    client.close()
    return rows._raw;

def coinStat30(coinname):
    rows = None
    client = None
    client = InfluxDBClient(host, port, user, password, dbname)
    sql = "SELECT * FROM CoinStatus where Serial = '1' and COIN = "+"'"+coinname+"'"+" order by time desc limit 30 tz('Asia/Seoul')"
    rows = client.query(sql)
    client.close()
    return rows._raw;

def coinStat10(coinname):
    rows = None
    client = None
    client = InfluxDBClient(host, port, user, password, dbname)
    sql = "SELECT * FROM CoinStatus where Serial = '1' and COIN = "+"'"+coinname+"'"+" order by time desc limit 10 tz('Asia/Seoul')"
    rows = client.query(sql)
    client.close()
    return rows._raw;

def coinRate10(coinname):
    rows = None
    client = None
    client = InfluxDBClient(host, port, user, password, dbname)
    sql = "SELECT * FROM CoinStatus where COIN = "+"'"+coinname+"'"+" order by time desc limit 150 tz('Asia/Seoul')"
    rows = client.query(sql)
    client.close()
    return rows._raw;

def coinRate30(coinname):
    rows = None
    client = None
    client = InfluxDBClient(host, port, user, password, dbname)
    sql = "SELECT * FROM CoinStatus where COIN = "+"'"+coinname+"'"+" order by time desc limit 450 tz('Asia/Seoul')"
    rows = client.query(sql)
    client.close()
    return rows._raw;

def coinRate60(coinname):
    rows = None
    client = None
    client = InfluxDBClient(host, port, user, password, dbname)
    sql = "SELECT * FROM CoinStatus where COIN = "+"'"+coinname+"'"+" order by time desc limit 900 tz('Asia/Seoul')"
    rows = client.query(sql)
    client.close()
    return rows._raw;

def coinCombo():
    coins = []
    coinlist = pyupbit.get_tickers()
    for coin in coinlist:
        if coin.startswith("KRW"):
            coins = coins + [coin]
        else:
            pass
    return coins;

def getScore10():
    row = None
    client = None
    coins = []
    rows = []
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
    rows = rows[0:3]
    for trade in rows:
        price = trade["Price"]
        coin = trade["COIN"]
        ret = upbit.buy_market_order(coin,10000)
        orders = orders + list(ret)
    return orders;

def sell10():
    access = "AT7HeOx48ZzzRDTO5y6FA2Lmw12ufGHwWArU5xVz"
    secret = "b4Qg0uZaapuTk18Q7qESC4AQIVboTI9HAhduY4SD"
    rows = []
    upbit = pyupbit.Upbit(access, secret)
    bal = upbit.get_balances()
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
                tprice = int(float(cfs["avg_buy_price"])*1.002)
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
                    tprice = tprice
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