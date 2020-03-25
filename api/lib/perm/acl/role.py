# -*- coding:utf-8 -*-

import six

from api.models.acl import Role
from api.extensions import db
from api.lib.perm.acl.cache import RoleCache
from api.lib.perm.acl.cache import RoleRelationCache
from api.models.acl import RoleRelation




class RoleRelationCRUD(object):
    @staticmethod
    def get_parents(rids=None, uids=None):
        rid2uid = dict()
        print(rids,uids)
        if uids is not None:
            uids = [uids] if isinstance(uids, six.integer_types) else uids
            rids = db.session.query(Role).filter(Role.deleted.is_(False)).filter(Role.uid.in_(uids))
            rid2uid = {i.id: i.uid for i in rids}
            rids = [i.id for i in rids]
        else:
            rids = [rids] if isinstance(rids, six.integer_types) else rids

        res = db.session.query(RoleRelation).filter(
            RoleRelation.child_id.in_(rids)).filter(RoleRelation.deleted.is_(False))
        id2parents = {}
        for i in res:
            id2parents.setdefault(rid2uid.get(i.child_id, i.child_id), []).append(RoleCache.get(i.parent_id).to_dict())

        return id2parents

    @staticmethod
    def get_parent_ids(rid):
        res = RoleRelation.get_by(child_id=rid, to_dict=False)
        print(res,"res:-===================")
        return [i.parent_id for i in res]

    @staticmethod
    def get_child_ids(rid):
        res = RoleRelation.get_by(parent_id=rid, to_dict=False)

        return [i.parent_id for i in res]

    @classmethod
    def recursive_parent_ids(cls, rid):
        print(cls,'-----------------',rid)
        all_parent_ids = set()

        def _get_parent(_id):
            all_parent_ids.add(_id)
            parent_ids = RoleRelationCache.get_parent_ids(_id)
            print(parent_ids)
            for parent_id in parent_ids:
                _get_parent(parent_id)

        _get_parent(rid)

        return all_parent_ids

    @classmethod
    def recursive_child_ids(cls, rid):
        all_child_ids = set()

        def _get_children(_id):
            all_child_ids.add(_id)
            child_ids = RoleRelationCache.get_child_ids(_id)
            for child_id in child_ids:
                _get_children(child_id)

        _get_children(rid)

        return all_child_ids

    @staticmethod
    def add(parent_id, child_id):
        RoleRelation.get_by(parent_id=parent_id, child_id=child_id) and abort(400, "It's already existed")

        RoleRelationCache.clean(parent_id)
        RoleRelationCache.clean(child_id)

        return RoleRelation.create(parent_id=parent_id, child_id=child_id)

    @classmethod
    def delete(cls, _id):
        existed = RoleRelation.get_by_id(_id) or abort(400, "RoleRelation <{0}> does not exist".format(_id))

        child_ids = cls.recursive_child_ids(existed.child_id)
        for child_id in child_ids:
            role_rebuild.apply_async(args=(child_id,), queue=ACL_QUEUE)

        RoleRelationCache.clean(existed.parent_id)
        RoleRelationCache.clean(existed.child_id)

        existed.soft_delete()

    @classmethod
    def delete2(cls, parent_id, child_id):
        existed = RoleRelation.get_by(parent_id=parent_id, child_id=child_id, first=True, to_dict=False)
        existed or abort(400, "RoleRelation < {0} -> {1} > does not exist".format(parent_id, child_id))

        child_ids = cls.recursive_child_ids(existed.child_id)
        for child_id in child_ids:
            role_rebuild.apply_async(args=(child_id,), queue=ACL_QUEUE)

        RoleRelationCache.clean(existed.parent_id)
        RoleRelationCache.clean(existed.child_id)

        existed.soft_delete()