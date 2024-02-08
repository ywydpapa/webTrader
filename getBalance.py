import pyupbit

access = "AT7HeOx48ZzzRDTO5y6FA2Lmw12ufGHwWArU5xVz"
secret = "b4Qg0uZaapuTk18Q7qESC4AQIVboTI9HAhduY4SD"
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balances())     # KRW-BTC 조회
