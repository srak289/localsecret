from sqlalchemy import Boolean, Integer, String, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr

from datetime import datetime

__all__ = []

@as_declarative()
class Base(object):

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        cls_name = ''
        for i,x in enumerate(cls.__name__):
            if i > 0 and x.isupper():
                cls_name += f'_{x.lower()}'
            elif i == 0:
                cls_name += x.lower()
            else:
                cls_name += x
        return cls_name

    @declared_attr
    def timestamp(self):
        return Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

