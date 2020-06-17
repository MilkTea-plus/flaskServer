"""
Created on 2020年3月20日

@author: xxx
"""
import decimal
import json
import jpype
from threading import Thread
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
cache = Cache()


# float double类型转换
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def CostCalculator(formula):
    # 指定main class
    cost_calculator_class = jpype.JClass("com.jjh.calculator.CostCalculator")
    # 创建类实例对象
    jd = cost_calculator_class(formula)
    return jd


# 装饰器,用于异步处理,包含sqlalchemy无法使用异步处理
def decorator(function):
    def wrapper(*args, **kwargs):
        thr = Thread(target=function, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
