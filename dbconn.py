from influxdb import InfluxDBClient

host = '192.168.108.147'
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