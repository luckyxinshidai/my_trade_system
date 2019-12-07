if bar.datetime == datetime.strptime("2019-03-01,13:31", "%Y-%m-%d,%H:%M"):
    print bar.datetime.strftime("%Y-%m-%d,%H:%M")
    print bar.open
    print bar.high
    print bar.low
    print bar.close
    self.buy(bar.close, 2)
if bar.datetime == datetime.strptime("2019-03-01,14:36", "%Y-%m-%d,%H:%M"):
    print bar.datetime.strftime("%Y-%m-%d,%H:%M")
    print bar.open
    print bar.high
    print bar.low
    print bar.close
    self.sell(bar.close, 2)