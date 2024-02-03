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

while True:
    coinNames = pyupbit.get_tickers()
    for coinName in coinNames:
        if coinName.startswith("KRW"):
            sql = "SELECT * FROM CoinStatus where Serial = '1' and COIN = "+"'"+coinName+"'"+" order by time desc limit 30 tz('Asia/Seoul')"
            row = list(client.query(sql))
            score = 100
            for i in range(29,-1,-1):
                line = row[0][i]
                score = score * float(line["BuyRate"])/100
                if score < 10:
                    score = score + 5
                elif score > 1000:
                    score = score/3
            print(line["COIN"])
            print("SCORE : ",score)
            print(line["ask_price"])
            print(line["TimeStamp"])
            measurement = 'CoinRank'
            tags = {'COIN':line["COIN"], 'TimeStamp':line["TimeStamp"]}
            fields = {'Score': score, 'Price':line["ask_price"]}
            insdata = [{'measurement':measurement, 'tags':tags, 'fields':fields}]
            client.write_points(insdata)
        else:
            pass
    client.close()
    time.sleep(60)
