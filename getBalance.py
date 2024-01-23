import pyupbit

access = "AT7HeOx48ZzzRDTO5y6FA2Lmw12ufGHwWArU5xVz"
secret = "b4Qg0uZaapuTk18Q7qESC4AQIVboTI9HAhduY4SD"
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-BTC 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
print(upbit.get_order("KRW-XRP",state='wait'))
print(pyupbit.get_orderbook("KRW-XRP"))
print(pyupbit.get_tickers())
