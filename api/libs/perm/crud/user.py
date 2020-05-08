from api.models.account import User
from api.libs.cache import UserCache
class UserCRUD(object):
    '''
        User相关的增删改查
    '''
    
    @staticmethod
    def update(id, **kwargs):
        user = User.get_by(id=id, to_dict=False, first=True) or abort(404, "User <{0}> does not exist".format(id))
        print(user,'=======================')
        if kwargs.get("username"):
            other = User.get_by(username=kwargs['username'], first=True, to_dict=False)
            if other is not None and other.uid != user.uid:
                return abort(400, "User <{0}> cannot be duplicated".format(kwargs['username']))

        UserCache.clean(user)

        return user.update(**kwargs)

