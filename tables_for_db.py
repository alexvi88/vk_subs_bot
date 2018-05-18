from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class user_groups(Base): 
    __tablename__ = 'user_groups'
    
    group_id = Column(String, primary_key=True)
    group_last_time = Column(Integer)

    def __init__(self, _group_id):
        self.group_id = _group_id

        now_d = datetime.datetime.now()
        self.group_last_time = int(now_d.timestamp())

    def __repr__(self):
        return str(self.group_id)

    def __str__(self):
        return str(self.group_id)
        
