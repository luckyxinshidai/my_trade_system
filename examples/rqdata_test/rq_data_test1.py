import rqdatac as rq
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from rqdatac import *
rq.init()
# rq.all_instruments(type='Future')
# future_data = rq.all_instruments(type="Future")
# future_data_to_csv = pd.DataFrame(future_data)
# future_data_to_csv.to_csv("all_future1.csv")
# rb_dominant_list = rq.get_dominant_future('rb', end_date='20181213')
# rb_dominant_list_to_csv = pd.DataFrame(rb_dominant_list)
# rb_dominant_list_to_csv.to_csv("rb_dominant_list.csv")
# rb_dominant_list_to_csv = pd.DataFrame.from_csv("rb_dominant_list.csv")
rb_dominant_list_to_csv = pd.read_csv("rb_dominant_list.csv")
rb_unique = rb_dominant_list_to_csv['dominant']
rb_unique = rb_unique.unique()
print rb_unique
for d in rb_unique:
    temp_data = rq.get_price(d, start_date='2009-3-27', end_date='2018-11-28', frequency='1m')
    temp_data_frame = pd.DataFrame(temp_data)
    file_name = d + "_data_dataframe.csv"
    temp_data_frame.to_csv(file_name)
    print d + "data have been load over\n"
# rb0000_data = rq.get_price('RB1901', start_date='2009-3-27', end_date='2018-11-28', frequency='1m')
# rb0000_data_dataframe = pd.DataFrame(rb0000_data)
# rb0000_data_dataframe.to_csv("RB1901_data_dataframe.csv")

