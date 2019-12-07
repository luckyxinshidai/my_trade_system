# encoding: UTF-8

import rqdatac as rq
import pandas as pd
import sys
import datetime
import os


DATA_PATH = "E:\\future_data\\main_contract\\"
reload(sys)
loop_count = 0
sys.setdefaultencoding('utf8')
rq.init()
need_to_monitor_future_list = ['RB', 'TA', 'CF', 'L', 'PP', 'M', 'Y', 'AG', 'MA', 'SR']
time_of_today = datetime.datetime.now().strftime("%Y%m%d")


def check_file_path():
    if os.path.exists(DATA_PATH):
        return
    else:
        os.makedirs(DATA_PATH)


def get_main_contract_price(future):
    future_name = future + "88"
    test_data = rq.get_price(future_name, end_date=time_of_today, frequency='1m')
    test_data = pd.DataFrame(test_data)
    save_file_name = future + "0000" + ".csv"
    test_data.to_csv(DATA_PATH + save_file_name)


def traverse_all_future():
    for future in need_to_monitor_future_list:
        get_main_contract_price(future)


if __name__ == '__main__':
    check_file_path()
    traverse_all_future()



