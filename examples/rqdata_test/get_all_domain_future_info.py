# encoding: UTF-8
import rqdatac as rq
from rqdatac import *
import pandas as pd
import sys
import datetime
import os


DATA_PATH = "E:\\future_data\\all_data\\"
NO_MAKER_DATA_PATH = "other_table\\"
SAVE_PATH = DATA_PATH + NO_MAKER_DATA_PATH
reload(sys)
loop_count = 0
sys.setdefaultencoding('utf8')
rq.init()
need_to_monitor_future_list = ['RB', 'TA', 'CF', 'L', 'PP', 'M', 'Y', 'AG', 'MA', 'SR']
margin_rate_list = []
contract_multiplier_list = []
symbol_list = []
time_of_today = datetime.datetime.now().strftime("%Y%m%d")


def get_current_domain_future_info():
    for temp_future in need_to_monitor_future_list:
        temp_future_name = rq.get_dominant_future(temp_future, time_of_today)[-1]
        temp_info = rq.instruments(temp_future_name)
        margin_rate = temp_info.margin_rate     # 保证金率
        contract_multiplier = temp_info.contract_multiplier     # 合约乘数
        margin_rate_list.append(margin_rate)
        contract_multiplier_list.append(contract_multiplier)
        symbol_list.append(temp_future_name)
    all_future_margin_and_contract_multiplier = pd.DataFrame({'future_name': symbol_list,
                                                              'margin': margin_rate_list,
                                                              'contract_multiplier': contract_multiplier_list})
    all_future_margin_and_contract_multiplier.to_csv(SAVE_PATH+"all_future_margin_and_contract_multiplier.csv")


if __name__ == '__main__':
    get_current_domain_future_info()
