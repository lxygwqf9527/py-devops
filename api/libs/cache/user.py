from api.extensions import cache
from api.models.account import User, Role,  Notify

class UserCache(object):
    '''
        用户相关的缓存类
    '''
    PREFIX_ID = "User:id:{0}"
    PREFIX_NAME = "User:username:{0}"
    PREFIX_NICK = "User:nickname:{0}"
    PREFIX_ERROR = "User:error:{0}"
    
    @classmethod
    def get(cls, key):
        '''
        获取key，获取不到就设置
        '''
        user = cache.get(cls.PREFIX_ID.format(key)) or \
               cache.get(cls.PREFIX_NAME.format(key)) or \
               cache.get(cls.PREFIX_NICK.format(key))
        if not user:
            user = User.query.get(key) or \
                   User.query.get_by_username(key) or \
                   User.query.get_by_nickname(key)
        if user:
            cls.set(user)
        return user
    
    @classmethod
    def set(cls, user):
        '''
        设置key
        '''
        cache.set(cls.PREFIX_ID.format(user.id), user)
        cache.set(cls.PREFIX_NAME.format(user.username), user)
        cache.set(cls.PREFIX_NICK.format(user.nickname), user)
    
    @classmethod
    def clean(cls, user):
        '''
        清除key
        '''
        cache.delete(cls.PREFIX_ID.format(user.id))
        cache.delete(cls.PREFIX_NAME.format(user.username))
        cache.delete(cls.PREFIX_NICK.format(user.nickname))
        
    @classmethod
    def set_count_error(cls,key,value):
        cache.set(cls.PREFIX_ERROR.format(key), value)
    
    @classmethod
    def get_count_error(cls,key):
        value = cache.get(cls.PREFIX_ERROR.format(key))
        if not value:
            cls.set_count_error(key,1)
            value = cache.get(cls.PREFIX_ERROR.format(key))
        else:
            cls.set_count_error(key,value+1)
            
        return value
    
    @classmethod
    def del_count_error(cls,key):
        cache.delete(cls.PREFIX_ERROR.format(key))


class PermissionCache(object):
    PREFIX_ID = "Permission:id:{0}"

    @classmethod
    def get(cls, id):
        permission = cache.get(cls.PREFIX_ID.format(key))

        if not permission:
            permission = Role.get_by(id=id).page_perms

        if permission:
            cls.set(id,permission)
        
        return permission
    
    @classmethod
    def set(cls, id, permission):
        cache.set(cls.PREFIX_ID.format(id),permission)
        
class NotifyCache(object):
    '''
        通知相关的缓存类
    '''
    PREFIX_QUIET = "Notify:quiet"

    @classmethod
    def set_by_time(cls, time):
        cache.set(cls.PREFIX_QUIET, time)
    
    @classmethod
    def get_by_time(cls, time):
        return cache.get(cls.PREFIX_QUIET)

