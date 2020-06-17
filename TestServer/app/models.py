"""
Created on 2020年3月11日

@author: xxx
"""
from sqlalchemy.dialects.mysql import DOUBLE
from app.common import DecimalEncoder, db
import json


class User:
    """采样快照头"""
    __tablename__ = "user"
    user_id = db.Column(db.BigInteger, primary_key=True, nullable=False)  # 主键
    user_name = db.Column(db.String, nullable=False)  # 用户名
    user_salary = db.Column(DOUBLE, nullable=True)  # 用户薪水

    def to_json(self):
        return {
            "userId": self.user_id,
            "userName": self.user_name,
            "userSalary": json.dumps(self.user_salary, cls=DecimalEncoder)
        }

    def __init__(self, user_id, user_name, user_salary):
        self.user_id = user_id
        self.user_name = user_name
        self.user_salary = user_salary
