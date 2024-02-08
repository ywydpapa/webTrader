import pyupbit
import time
from influxdb import InfluxDBClient

envhost = 'localhost'
envuser = 'root'
envpassword = 'root'
envdb = 'swc'
envport = 8086
client = InfluxDBClient(envhost,envport, envuser, envpassword, envdb)

while True:
    coinNames = pyupbit.get_tickers(fiat="KRW")
    for coinName in coinNames:
        try:
            sql = "SELECT * FROM CoinStatus where Serial = '1' and COIN = "+"'"+coinName+"'"+" order by time desc limit 60 tz('Asia/Seoul')"
            row = list(client.query(sql))
            score = 100
            for i in range(29,-1,-1):
                line = row[0][i]
                score = score * float(line["BuyRate"])/100
                if score < 10:
                    score = score + 10
                elif score > 1000:
                    score = score/4.5
            measurement = 'CoinRank'
            tags = {'COIN':line["COIN"], 'TimeStamp':line["TimeStamp"]}
            fields = {'Score': score, 'Price':line["bid_price"]}
            insdata = [{'measurement':measurement, 'tags':tags, 'fields':fields}]
            client.write_points(insdata)
        except Exception as ex:
            print("Error : ",ex)
            break
    client.close()
    time.sleep(60)
