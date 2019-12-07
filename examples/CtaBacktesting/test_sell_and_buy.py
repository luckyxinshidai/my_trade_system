# encoding: UTF-8

"""
这里的Demo是一个最简单的双均线策略实现
"""

from __future__ import division

from vnpy.trader.vtConstant import EMPTY_STRING, EMPTY_FLOAT
from vnpy.trader.app.ctaStrategy.ctaTemplate import (CtaTemplate, 
                                                     BarGenerator,
                                                     ArrayManager)
from datetime import datetime
import numpy as np
import talib
from pattern_recognition import k_line_pattern
# import rqdatac as rq


########################################################################
class DoubleMaStrategy(CtaTemplate):
    """双指数均线策略Demo"""
    className = 'DoubleMaStrategy'
    author = u'用Python的交易员'
    
    # 策略参数
    fastWindow = 5     # 快速均线参数
    first_N = 0
    pre_N = 0
    current_N = 0
    length_of_N = 20
    PDC = 0
    slowWindow = 20     # 慢速均线参数
    long_window = 144   # 长趋势
    initDays = 10       # 初始化数据所用的天数
    unit_size_of_position = 0   # 头寸规模，根据海龟交易法则进行制定，每天变化，无持仓变化
    future_name = "RB"
    new_day = True
    total_capital = 100000
    donchian_up = 0
    donchian_down = 0
    stop_donchian_up = 0
    stop_donchian_down = 0
    buy_open_price = 0
    buy_append_price = 0
    sell_open_price = 0
    sell_append_price = 0

    # 策略参数
    long_window = 144  # 长趋势


    longMA0 = EMPTY_FLOAT
    longMA1 = EMPTY_FLOAT

    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbol',
                 'fastWindow',
                 'slowWindow']    
    
    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos',
               'fastMa0',
               'fastMa1',
               'slowMa0',
               'slowMa1']  
    
    # 同步列表，保存了需要保存到数据库的变量名称
    syncList = ['pos']

    #----------------------------------------------------------------------
    def __init__(self, ctaEngine, setting):
        """Constructor"""
        super(DoubleMaStrategy, self).__init__(ctaEngine, setting)
        
        self.bg = BarGenerator(self.onBar)
        self.am = ArrayManager()
        self.bg15 = BarGenerator(self.onBar, 15, self.on15MinBar)
        self.am15 = ArrayManager()
        self.bg5 = BarGenerator(self.onBar, 5, self.on5MinBar)
        self.am5 = ArrayManager()
        # rq.init()
        
        # 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
        # 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
        # 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
        # 策略时方便（更多是个编程习惯的选择）
        
    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略初始化')
        
        initData = self.loadBar(self.initDays)
        for bar in initData:
            self.onBar(bar)
        
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略启动')
        self.putEvent()
    
    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        self.writeCtaLog(u'双EMA演示策略停止')
        self.putEvent()
        
    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        self.bg.updateTick(tick)
        
    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        self.bg15.updateBar(bar)
        self.bg5.updateBar(bar)
        am = self.am        
        am.updateBar(bar)
        if not am.inited:
            return
        if not self.am15.inited:
            return
        if not self.unit_size_of_position:
            self.get_unit_size_of_position()
        if not self.donchian_up:
            (self.donchian_up, self.donchian_down) = am.donchian(300)  # 15 *20
            (self.stop_donchian_up, self.stop_donchian_down) = am.donchian(150)  # 15 * 10
            return  # 没有计算过通道之前不进行交易判断
        # TODO 先使用最简单的入市策略，后续再根据海龟策略的系统1中的讲解，添加入市的策略
        long_ma = am.sma(self.long_window, array=True)
        self.longMA0 = long_ma[-1]
        self.longMA1 = long_ma[-2]
        rising_trend = self.longMA0 > self.longMA1
        down_trend = self.longMA0 < self.longMA1

        if am.high[-1] > self.donchian_up and self.pos == 0 and rising_trend:    # 超出通道上线买入
            self.buy(am.close[-1], 1)
            self.buy_open_price = am.close[-1]
            self.buy_append_price = self.buy_open_price
        if am.low[-1] < self.donchian_down and self.pos == 0 and down_trend:   # 跌穿通道下沿卖出
            self.short(am.close[-1], 1)
            self.sell_open_price = am.close[-1]
            self.sell_append_price = self.sell_open_price
        # 加仓逻辑
        if self.pos:
            # 多头加仓
            if 4 > self.pos > 0:
                if am.high[-1] >= (self.buy_append_price + self.current_N/2):
                    self.buy(am.close[-1], 1)
                    self.buy_append_price = am.close[-1]
            if -4 < self.pos < 0:
                if am.low[-1] <= (self.sell_append_price - self.current_N/2):
                    self.short(am.close[-1], 1)
                    self.sell_append_price = am.close[-1]
        # 退出逻辑
        if self.pos:
            if self.pos > 0:
                if am.close[-1] < self.stop_donchian_down:
                    self.sell(am.close[-1], abs(self.pos))
            if self.pos < 0:
                if am.close[-1] > self.stop_donchian_up:
                    self.cover(am.close[-1], abs(self.pos))
        # 止损逻辑
        if self.pos:
            if self.pos > 0:
                if am.close[-1] < self.buy_append_price - 2 * self.current_N:
                    self.sell(am.close[-1], abs(self.pos))
            if self.pos < 0:
                if am.close[-1] > self.sell_append_price + 2 * self.current_N:
                    self.cover(am.close[-1], abs(self.pos))

        (self.donchian_up, self.donchian_down) = am.donchian(300)  # 15 *20
        (self.stop_donchian_up, self.stop_donchian_down) = am.donchian(150)  # 15 * 10

        # 发出状态更新事件
        self.putEvent()

    def on15MinBar(self, bar):
        """15分钟K线推送"""
        self.am15.updateBar(bar)
        if not self.am15.inited:
            return
        my_15_min_bar = self.am15
        # hammer = talib.CDLHAMMER(my_15_min_bar.open[-1:], my_15_min_bar.high[-1:],
        #                          my_15_min_bar.low[-1:], my_15_min_bar.close[-1:])
        # inverted_hammer = talib.CDLINVERTEDHAMMER(my_15_min_bar.open[-1:], my_15_min_bar.high[-1:],
        #                          my_15_min_bar.low[-1:], my_15_min_bar.close[-1:])

        # if my_15_min_bar.open[-1:] == my_15_min_bar.low[-1:] and my_15_min_bar.low[-1:] == my_15_min_bar.close[-1:]:
        #     if my_15_min_bar.high[-1:] > my_15_min_bar.open[-1:]:
        #         print "hammer: ",
        #         print bar.datetime.strftime("%Y-%m-%d,%H:%M")
        # if inverted_hammer[-1]:
        #     print "inverted_hammer: ",
        #     print bar.datetime.strftime("%Y-%m-%d,%H:%M")
        # if hammer[-1]:
        #     print bar.datetime.strftime("%Y-%m-%d,%H:%M")
#        if self.am15.close[-20] > 1:    # 一共有了20根bar再进行指标的计算
#            print bar.datetime.strftime("%Y-%m-%d,%H:%M")
#            print self.am15.close[-20:]
        hammer = k_line_pattern.hammer(my_15_min_bar.open[-1:], my_15_min_bar.high[-1:],
                                       my_15_min_bar.low[-1:], my_15_min_bar.close[-1:])
        if hammer:
            print "hammer: ",
            print bar.datetime.strftime("%Y-%m-%d,%H:%M")
        if not self.first_N:
            self.calculate_first_N()
        if not self.pre_N:
            self.pre_N = self.first_N
            self.current_N = self.pre_N     # 期初使用preN 作为 currentN
        else:
            self.current_N = (self.pre_N * 19 + self.calculate_TR())/self.length_of_N
            self.pre_N = self.current_N

    def calculate_TR(self):
        current_day_H_minus_L = self.am15.high[-1] - self.am15.low[-1]
        current_day_H_minus_yesterday_C = abs(self.am15.high[-1] - self.am15.close[-2])
        yesterday_C_minus_current_day_L = abs(self.am15.close[-2] - self.am15.low[-1])
        TR = max(current_day_H_minus_L, current_day_H_minus_yesterday_C, yesterday_C_minus_current_day_L)
        return TR

    def on5MinBar(self, bar):
        """5分钟K线推送"""
        self.am5.updateBar(bar)
        if not self.am5.inited:
            return
        my_15_min_bar = self.am5
        # hammer = talib.CDLHAMMER(my_15_min_bar.open[-1:], my_15_min_bar.high[-1:],
        #                          my_15_min_bar.low[-1:], my_15_min_bar.close[-1:])
        # inverted_hammer = talib.CDLINVERTEDHAMMER(my_15_min_bar.open[-1:], my_15_min_bar.high[-1:],
        #                          my_15_min_bar.low[-1:], my_15_min_bar.close[-1:])
        # if my_15_min_bar.open[-1:] == my_15_min_bar.low[-1:] and my_15_min_bar.low[-1:] == my_15_min_bar.close[-1:]:
        #     if my_15_min_bar.high[-1:] > my_15_min_bar.open[-1:]:
        #         print "hammer: ",
        #         print bar.datetime.strftime("%Y-%m-%d,%H:%M")
        #
        # if inverted_hammer[-1]:
        #     print "inverted_hammer: ",
        #     print bar.datetime.strftime("%Y-%m-%d,%H:%M")
        # if hammer[-1]:
        #     print bar.datetime.strftime("%Y-%m-%d,%H:%M")
    # 用前二十一天的数据计算第一个N值
    def calculate_first_N(self):
        TR_list = []
        for i in range(-20, 0):
            current_day_H_minus_L = self.am15.high[i] - self.am15.low[i]
            current_day_H_minus_yesterday_C = abs(self.am15.high[i] - self.am15.close[i - 1])
            yesterday_C_minus_current_day_L = abs(self.am15.close[i - 1] - self.am15.low[i])
            TR = max(current_day_H_minus_L, current_day_H_minus_yesterday_C, yesterday_C_minus_current_day_L)
            TR_list.append(TR)
        self.first_N = np.array(TR_list).mean()

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        pass
    
    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        # 对于无需做细粒度委托控制的策略，可以忽略onOrder
        pass
    
    #----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass    

    def get_unit_size_of_position(self):
        if self.new_day and not self.pos:
            time_of_today = datetime.now().strftime("%Y%m%d")
            # 验证策略暂时先不管这一块儿，后续耗时的操作都在开盘前一个小时做好，然后策略从本地文件中读取数据
            # 在数据库中记录策略上一次运行的时间，用来判断是否需要重新计算unit_size_of_position
            # temp_future_name = rq.get_dominant_future(self.future_name, time_of_today)[-1]
            # temp_info = rq.instruments(temp_future_name)
            # margin_rate = temp_info.margin_rate
            # contract_multiplier = temp_info.contract_multiplier  # 合约乘数
            contract_multiplier = 10
            margin_rate = 0.09
            self.unit_size_of_position = (0.01 * self.total_capital) / (self.current_N * contract_multiplier)
            self.unit_size_of_position = self.unit_size_of_position * margin_rate * 2   # 期货公司收取的保证金率为最低的三倍左右
            self.unit_size_of_position = int(self.unit_size_of_position)


