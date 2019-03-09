# encoding: UTF-8

import csv
from datetime import datetime, timedelta
from time import time
import pymongo
from vnpy.trader.vtObject import VtBarData
import os
from vnpy.trader.app.ctaStrategy.ctaBase import MINUTE_DB_NAME


client = pymongo.MongoClient('127.0.0.1', 27017)
need_to_monitor_future_list = ['RB', 'TA', 'CF', 'L', 'PP', 'M', 'Y', 'AG', 'MA', 'SR']
DATA_PATH = "E:\\future_data\\all_data\\"


#def test_create_mongodb_index():
#    # collection.create_index([("datetime", pymongo.ASCENDING)], unique=True)
#    # collection.create_index('datetime', unique=True, name='datetime')
#    # collection.ensure_index('time', unique=True)
#
#
#def test_get_all_indexes():
#    for index in collection.list_indexes():
#        print(index)
#
#
#def test_drop_mongodb_index():
#    collection.drop_index("datetime_1")
#
#
#def get_max_min_time():
#    get_max_command = '[{$group : {_id : "$by_user", num_tutorial : {$max : "$likes"}}}]'
#    pipline = [{"$group": {"_id": "$datetime", "num_tutorial": {"$max": "$datetime"}}}]
#    # test = collection.aggregate(pipline)
#    test = collection.find_one(sort=[("datetime", -1)])["datetime"]     # max
#    print("Max time is :")
#    print(test)
#    test = collection.find_one(sort=[("datetime", 1)])["datetime"]  # min
#    print("Min time is :")
#    print(test)
#
#
#if __name__ == '__main__':
#    # test_create_mongodb_index()
#    # test_drop_mongodb_index()
#    # test_get_all_indexes()
#    get_max_min_time()
#    client.close()


def load_rq_csv(fileName, dbName, symbol):
    """将rqdata导出的csv格式的历史数据插入到Mongo数据库中"""
    start = time()
    print(u'开始读取CSV文件%s中的数据插入到%s的%s中' % (fileName, dbName, symbol))

    # 锁定集合，并创建索引
    collection = client[dbName][symbol]
    collection.ensure_index([('datetime', pymongo.ASCENDING)], unique=True)

    # 读取数据和插入到数据库
    with open(fileName, 'r') as f:
        reader = csv.DictReader(f)
        for d in reader:
            bar = VtBarData()
            bar.vtSymbol = symbol
            bar.symbol = symbol
            bar.open = float(d['open'])
            bar.high = float(d['high'])
            bar.low = float(d['low'])
            bar.close = float(d['close'])
            bar.date = datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')
            bar.time = datetime.strptime(d['datetime'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
            bar.datetime = datetime.strptime(bar.date + ' ' + bar.time, '%Y%m%d %H:%M:%S')
            bar.volume = d['volume']
            bar.openInterest = d['open_interest']

            flt = {'datetime': bar.datetime}
            collection.update_one(flt, {'$set': bar.__dict__}, upsert=True)
            print(bar.date, bar.time)

    print(u'插入完毕，耗时：%s' % (time() - start))


def find_all_csv_and_save_to_mongodb():
    for temp_contact in need_to_monitor_future_list:
        current_dir = DATA_PATH + temp_contact
        print(current_dir)
        index = 1
        for root, subdirs, files in os.walk(current_dir):
            print "第", index, "层"
            index += 1
            for filepath in files:
                file_name = os.path.join(root, filepath)
                symbol = os.path.basename(filepath)
                symbol = os.path.splitext(symbol)[0]
                print symbol
                load_rq_csv(file_name, MINUTE_DB_NAME, symbol)
                

if __name__ == '__main__':
    find_all_csv_and_save_to_mongodb()
