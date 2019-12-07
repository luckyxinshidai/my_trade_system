# -*- coding: utf-8 -*-
import pymongo
import re


myclient = pymongo.MongoClient("mongodb://localhost:27017/")


def re_test():
    test_a = re.match('12', 'RB1902')
    if test_a:
        print("hello world")
    print(test_a)


def test_mongodb():
    print("hello world")
    rb_list = []
    dblist = myclient.list_database_names()
    mydb = myclient['VnTrader_1Min_Db']
    collist = mydb.list_collection_names()
    for collect_name in collist:
        if re.match('RB', collect_name):
            rb_list.append(collect_name)
    rb_list.sort()
    return rb_list


# 分钟数据合成日线
def min_to_day():
    print(test_mongodb())


if __name__ == '__main__':
    # test_mongodb()
    # re_test()
    min_to_day()