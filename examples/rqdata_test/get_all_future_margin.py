# encoding: UTF-8
import rqdatac as rq
import pandas as pd
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')
rq.init()
count = 0
all_future_dataframe_columns = ['date', 'future_name', 'margin', 'open_interest', 'open_interest_price']
date_list = []
future_name_list = []
margin_list = []
open_interest_list = []
open_interest_price_list = []
DATA_PATH = "E:\\future_data\\all_data\\"
NO_MAKER_DATA_PATH = "other_table\\"
original_all_future_table = pd.read_csv(DATA_PATH + NO_MAKER_DATA_PATH + "all_future.csv")
test1 = original_all_future_table['underlying_symbol'].drop_duplicates()
# 获取当天的日期并转换为rq需要的格式
time_of_today = datetime.datetime.now().strftime("%Y%m%d")
time_of_yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")
last_trading_day = rq.get_previous_trading_date(time_of_today, n=1)
# date_list.append(last_trading_day)
for temp_future_name in test1:
    # 获取截止当天为止每个期货品种的主力合约
    temp_dominant_list = rq.get_dominant_future(temp_future_name, end_date=last_trading_day)
    print "当前合约为：" + temp_future_name
    # 最新的主力合约对应的具体合约
    newest_domiant_contract = pd.DataFrame(temp_dominant_list)
    if 'dominant' in newest_domiant_contract.columns:
        if not newest_domiant_contract['dominant'].empty:
            newest_domiant_contract = pd.DataFrame(temp_dominant_list)['dominant'].unique()[-1]
        else:
            continue
    else:
        continue
    # 最新具体合约的当天收盘价
    yesterday_price = pd.DataFrame(rq.get_price(newest_domiant_contract, start_date=last_trading_day,
                                                end_date=last_trading_day, frequency='1d'))
    newest_domiant_contract_close_price = yesterday_price['close']
    newest_domiant_contract_open_interest = yesterday_price['open_interest']
    # 获取前一交易日收盘价
    if newest_domiant_contract_close_price.empty:
        newest_domiant_contract_close_price = 0
    else:
        newest_domiant_contract_close_price = newest_domiant_contract_close_price[-1]
    # 获取前一交易日持仓量
    if newest_domiant_contract_open_interest.empty:
        newest_domiant_contract_open_interest = 0
    else:
        newest_domiant_contract_open_interest = newest_domiant_contract_open_interest[-1]
    temp_info = rq.instruments(newest_domiant_contract)
    margin_rate = temp_info.margin_rate
    open_interest = newest_domiant_contract_open_interest
    # 计算持仓金额
    open_interest_price = open_interest * newest_domiant_contract_close_price
    contract_multiplier = temp_info.contract_multiplier
    # 保证金 = 当日收盘价 * 合约乘数 * 保证金率 * 期货公司一般收取两倍
    margin = newest_domiant_contract_close_price * margin_rate * contract_multiplier * 2
    print_str1 = str(newest_domiant_contract) + "`s margin is" + str(int(margin))
    count += 1
    print print_str1
    future_name_list.append(temp_future_name)
    margin_list.append(margin)
    open_interest_list.append(open_interest)
    open_interest_price_list.append(open_interest_price)

print str(count)
all_future_margin_and_open_interest = pd.DataFrame({'date': pd.Timestamp(last_trading_day),
                                                    'future_name': future_name_list,
                                                    'margin': margin_list,
                                                    'open_interest': open_interest_list,
                                                    'open_interest_price': open_interest_price_list})
all_future_margin_and_open_interest.to_csv("all_future_margin_and_open_interest.csv")
