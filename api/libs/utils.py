import json
import redis
from flask import current_app
from decimal import Decimal
from datetime import datetime, date as datetime_date
from functools import lru_cache

from api.models.settings import Setting

# 转换时间格式到字符串
def human_datetime(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d %H:%M:%S')

# 转换时间格式到字符串(天)
def human_date(date=None):
    if date:
        assert isinstance(date, datetime)
    else:
        date = datetime.now()
    return date.strftime('%Y-%m-%d')

# 继承自dict，实现可以通过.来操作元素
class AttrDict(dict):
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __delattr__(self, item):
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

# 解析时间类型的数据
def parse_time(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        if len(value) == 10:
            return datetime.strptime(value, '%Y-%m-%d')
        elif len(value) == 19:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    raise TypeError('Expect a datetime.datetime value')
