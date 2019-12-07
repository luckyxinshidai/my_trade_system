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
print("dblist is", end=" ")
print(dblist)
mydb = myclient["VnTrader_1Min_Db"]
db_collection_list = mydb.list_collection_names()
for index, item in enumerate(db_collection_list):
    print(re.search('.*[^0-9]', item).group())
