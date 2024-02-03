import json
from influxdb import InfluxDBClient
import pyupbit
from flask import jsonify

host = 'swc9004.iptime.org'
port = 8086
user = 'root'
password = 'root'
dbname = 'swc'

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
    for coin in coinlist:
        if coin.startswith("KRW"):
            sql = "SELECT * FROM CoinStatus where Serial = '1' and COIN = "+"'"+coin+"'"+" order by time desc limit 10 tz('Asia/Seoul')"
            row = list(client.query(sql))
            rows = rows + row
        else:
            pass
    client.close()
    print(rows)
    return rows;
