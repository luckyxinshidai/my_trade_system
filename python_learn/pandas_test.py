import pandas as pd
from pandas import Series ,DataFrame
import pymongo
import re
import csv
from datetime import datetime
from typing import TextIO

from vnpy.event import EventEngine
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import database_manager
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.object import BarData


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()
mydb = myclient["VnTrader_1Min_Db"]
my_collection = mydb["RB0000"]
current_symbol = "RB0000"
current_exchange = Exchange.SHFE
current_interval = Interval.MINUTE
current_gateway = "DB"
bars = []
for x in my_collection.find({}, {'_id': 0}).limit(5):
    bar = BarData(symbol=current_symbol, exchange=current_exchange, datetime=x['datetime'],
                  interval=current_interval, volume=x['volume'], open_price=x['open'],
                  high_price=x['high'], low_price=x['low'], close_price=x['close'],
                  gateway_name=current_gateway)
    bars.append(bar)
database_manager.save_bar_data(bars)

# print(x['close'])
# db_collection_list = mydb.list_collection_names()
# print(db_collection_list)
# symbol_list = []
# for item in db_collection_list:
#     symbol_list.append(re.search('.*[^0-9]', item).group())
# symbol_list_pd = pd.DataFrame(pd.unique(symbol_list)).to_csv("symbol_list.csv")
# mydb = myclient["runoobdb"]

# exchange_list = ["CFFEX",   # China Financial Futures Exchange
# "SHFE",   # Shanghai Futures Exchange
# "CZCE",   # Zhengzhou Commodity Exchange
# "DCE",]     # Dalian Commodity Exchange
#
# print(exchange_list)
# symbol_exchange = {
#
# }
# test_pd = pd.read_csv("./symbol_list.csv", encoding="gb2312")
# test_pd.drop(columns=0, axis=1, inplace=True)
# print(test_pd)