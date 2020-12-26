import time
import datetime
import get_instant_trades

ts = datetime.datetime.now().timestamp()
hey_inst = float(get_instant_trades.get_trades()[0])
hey_erc = float(get_instant_trades.get_erc_trades())

if abs(ts - hey_erc) >= 86400.0 and abs(ts - hey_inst) >= 86400.0:
    print('aaaaaaa')

'''print(abs(ts - hey_erc))
print(abs(ts - hey_inst))'''

'''s = "01/12/2011"
print(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
s2 = "02/12/2011"
print(time.mktime(datetime.datetime.strptime(s2, "%d/%m/%Y").timetuple()))
print(time.mktime(datetime.datetime.strptime(s2, "%d/%m/%Y").timetuple()) - time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))'''
