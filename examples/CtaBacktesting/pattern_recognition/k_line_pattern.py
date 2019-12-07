#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np


def hammer(open, high, low, close):
    open = np.array(open)[-1]
    high = np.array(high)[-1]
    low = np.array(low)[-1]
    close = np.array(close)[-1]
    # 锤子的第一个条件 实体处于整个价格区间的上端。而实体本身的颜色是无所谓的
    if open > low and close > low:
        condition1 = 1
    else:
        return 0
    # 锤子的第二个条件 下影线的长度至少达到实体高度的 2 倍
    abs_entity = abs(open - close)
    if open > close and ((abs_entity * 2) < (close - low)):
        condition2 = 1
    elif close > open and ((abs_entity * 2) < (open - low)):
        condition2 = 1
    else:
        return 0
    # 锤子的第三个条件 在这类蜡烛线中，应当没有上影线，即使有上影线，其长度也是极短的。
    # 目前取上影线小于实体的1/2
    if open > close and ((abs_entity/2) > (high - open)):
        condition3 = 1
    elif open < close and ((abs_entity/2) > (high - close)):
        condition3 = 1
    else:
        return 0
    print "open is " + str(int(open)) + " high is" + str(int(high)) + \
          " close is " + str(int(close)) + " low is " + str(int(low))
    return condition1 & condition2 & condition3