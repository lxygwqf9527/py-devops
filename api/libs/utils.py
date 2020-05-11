from datetime import datetime, date as datetime_date
import json


# 转换时间格式到字符串
def human_datetime(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')

# 继承自dict，实现可以通过.来操作元素
class AttrDict(dict):
    def __setattr__(self, key, value):
        print('set', key, value)
        self.__setitem__(key, value)

    def __getattr__(self, item):
        print('get', item)
        return self.__getitem__(item)

    def __delattr__(self, item):
        print('del','item')
        self.__delitem__(item)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime_date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, Decimal):
            return float(o)

        return json.JSONEncoder.default(self, o)