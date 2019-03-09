# encoding: UTF-8
import rqdatac as rq
import pandas as pd
import sys
import datetime
import os

DATA_PATH = "E:\\future_data\\all_data\\"
reload(sys)
loop_count = 0
sys.setdefaultencoding('utf8')
rq.init()
need_to_monitor_future_list = ['RB', 'TA', 'CF', 'L', 'PP', 'M', 'Y', 'AG', 'MA', 'SR']


def check_file_path():
    for temp in need_to_monitor_future_list:
        temp_path = DATA_PATH + temp
        if os.path.exists(temp_path):
            continue
        else:
            os.makedirs(temp_path)


def get_price_and_save_to_csv(a, temp):
    temp_path = DATA_PATH + temp
    for name, group in a:
        future_name = name
        start_date = group.index[0].strftime('%Y%m%d')
        end_date = group.index[-1].strftime('%Y%m%d')
        print future_name
        print start_date
        print end_date
        test_data = rq.get_price(future_name, start_date=start_date, end_date=end_date, frequency='1m')
        test_data = pd.DataFrame(test_data)
        save_file_name = future_name + ".csv"
        test_data.to_csv(temp_path + "\\" + save_file_name)


def get_all_future_and_save_data():
    format_today = datetime.datetime.now().strftime('%Y%m%d')
    for temp in need_to_monitor_future_list:
        temp_dominant_list = rq.get_dominant_future(temp.lower(), end_date=format_today)
        temp_dominant_list.sort_index(inplace=True)
        temp_dominant_list = pd.DataFrame(temp_dominant_list)
        a = temp_dominant_list.groupby('dominant')
        get_price_and_save_to_csv(a, temp)


if __name__ == '__main__':
    check_file_path()
    get_all_future_and_save_data()

