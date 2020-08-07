import json
import redis
from flask import current_app
from decimal import Decimal
from datetime import datetime, date as datetime_date
from functools import lru_cache

from api.models import Setting

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


class AppSetting:
    keys = ('public_key', 'private_key', 'mail_service', 'api_key', 'spug_key', 'ldap_service')

    @classmethod
    @lru_cache(maxsize=64)
    def get(cls, key):
        info = Setting.objects.filter(key=key).first()
        if not info:
            raise KeyError(f'no such key for {key!r}')
        return info.value

    @classmethod
    def get_default(cls, key, default=None):
        info = Setting.objects.filter(key=key).first()
        if not info:
            return default
        return info.value

    @classmethod
    def set(cls, key, value, desc=None):
        if key in cls.keys:
            Setting.objects.update_or_create(key=key, defaults={'value': value, 'desc': desc})
        else:
            raise KeyError('invalid key')

class RedisHandler(object):
    def __init__(self, flask_app=None):
        self.flask_app = flask_app
        self.r = None

    def init_app(self, app):
        self.flask_app = app
        config = self.flask_app.config
        try:
            pool = redis.ConnectionPool(
                max_connections=config.get("REDIS_MAX_CONN"),
                host=config.get("CACHE_REDIS_HOST"),
                port=config.get("CACHE_REDIS_PORT"),
                db=config.get("REDIS_DB"))
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            current_app.logger.warning(str(e))
            current_app.logger.error("init redis connection failed")

    def get(self, key_ids, prefix):
        try:
            value = self.r.hmget(prefix, key_ids)
        except Exception as e:
            current_app.logger.error("get redis error, {0}".format(str(e)))
            return
        return value

    def _set(self, obj, prefix):
        try:
            self.r.hmset(prefix, obj)
        except Exception as e:
            current_app.logger.error("set redis error, {0}".format(str(e)))

    def create_or_update(self, obj, prefix):
        self._set(obj, prefix)

    def delete(self, key_id, prefix):
        try:
            ret = self.r.hdel(prefix, key_id)
            if not ret:
                current_app.logger.warn("[{0}] is not in redis".format(key_id))
        except Exception as e:
            current_app.logger.error("delete redis key error, {0}".format(str(e)))