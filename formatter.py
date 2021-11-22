import pandas as pd
import datetime


class Labeller:
    @staticmethod
    def simple(stock):
        labels = []
        for i in range(1, 100):
            last = stock['Close'][i-1]
            cur = stock['Close'][i]
            if cur - last > 0:
                score = 1
            else:
                score = -1

            labels.append(score)
        return labels

    # input = {'t':...,'o':...}
    # res = ticker,dd,mm,yy,day,o,c,h,l,vol,label
    def alpacahist_to_list(self, stock):
        pass


class DatesFormat:
    # Date format like datetime.datetime.now()
    # Eg = datetime.datetime(2021, 11, 17, 16, 54, 57, 194018)
    # Rfc = '2015-1-1T07:20:50.52Z'
    @staticmethod
    def regulartrfc(date:datetime.datetime):
        dd = str(date.day)
        mm = str(date.month)
        year = str(date.year)
        time = str(date.hour) + ":"+str(date.minute) + ":" + str(date.second)

        res = year + '-' + mm + '-' + dd + 'T' + time+'Z'
        return res

    @staticmethod
    def easyRFC(dd,mm,yy):
        time = 'T12:00:00Z'

        res = yy + '-' + mm + '-' + dd + time
        return res

    # date format "mm dd yyyy"
    @staticmethod
    def get_day(date):
        # day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        # Encoded Date result corresponds to day above
        day = datetime.datetime.strptime(date, '%d %m %Y').weekday() + 1
        # print(day_name[day])
        return day

    # Date from 2020-11-11T05:00:00Z to list
    @staticmethod
    def rfc_list(date):
        tx = date[:date.find('T')]
        yyyy,mm,dd = list(map(int,tx.split('-')))
        date = str(dd) + ' ' + str(mm) + ' ' + str(yyyy)
        day_num = DatesFormat.get_day(date)
        return dd,mm,yyyy,day_num

class cleaners:
    def __init__(self):
        pass


if __name__ == '__main__':
    DatesFormat.get_day()