"""
Created on 2020年3月11日

@author: xxx
"""
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app.api import BluePrint
from app.common import cache, db
import jpype
import os

app = Flask(__name__)

app.register_blueprint(blueprint=BluePrint)

# sqlAlchemy的配置参数
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/dbname?charset=utf8?auth_plugin=mysql_native_password'
# 设置sqlAlchemy自动跟踪数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 打印SQL语句
app.config['SQLALCHEMY_ECHO'] = False
# cache配置
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'xxx.xxx.xxx.xxx'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_PASSWORD'] = 'root'

app.config['ENV'] = 'production'

# cache初始化
cache.init_app(app=app)

# 数据库初始化
db.init_app(app)


# Java虚拟机配置初始化
def initJvm():
    # 从环境变量获取jvm虚拟机安装路径，若不存在则获取默认路径
    if "JVM_PATH" in os.environ:
        jvm_path = os.environ["JVM_PATH"]
    else:
        jvm_path = jpype.getDefaultJVMPath()
    # 从环境变量获取Jar包路径，若不存在则获取绝对路径
    if "Jar_Path" in os.environ:
        jar_path = os.environ["Jar_Path"]
    else:
        jar_path = os.path.abspath('.')

    try:
        # 加载jar包
        jpype.startJVM(jvm_path, "-ea", "-Djava.class.path=%s" % (jar_path + '/Test.jar'))
    except:
        print('startJVM exception')
    return None


if __name__ == '__main__':
    # 判断数据库是否存在，不存在则新建
    engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/dbname?charset=utf8?auth_plugin=mysql_native_password")
    if not database_exists(engine.url):
        create_database(engine.url)
    # 自动建表
    db.create_all(app=app)

    # 启动Java虚拟机
    initJvm()

    # server运行的端口
    app.run(host='0.0.0.0', port=99, debug=True)
