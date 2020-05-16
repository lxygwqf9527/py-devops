# -*- coding:utf-8 -*-

from api.libs.cache.user import NotifyCache

class Notify(Model):
    TYPES = (
        ('1', '通知'),
        ('2', '待办'),
    )
    SOURCES = (
        ('monitor', '监控中心'),
        ('schedule', '任务计划'),
    )
    title = db.Column(db.String(255))
    source = db.Column(db.String(10), choices=SOURCES)
    type = db.Column(db.String(2), choices=TYPES)
    content = db.Column(db.String(255), nullable=True)
    unread = db.Column(db.Boolean,default=True)
    link = db.Column(db.Boolean, nullable=True)

    created_at = db.Column(db.string(20), default=human_datetime)

    @classmethod
    def make_notify(cls, source, type, title, content=None, with_quiet=True):
        if not with_quiet or time.time() - NotifyCache.get_by_time() > 3600:
            NotifyCache.set_by_time(time.time())
            self.create(source=source, title=title, type=type, content=content)

    def __str__(self):
        return '<Notify %r>' % self.title