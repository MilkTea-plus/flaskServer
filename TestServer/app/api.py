"""
Created on 2020年3月12日

@author: xxx
"""
import json
import time
import requests
from flask import Blueprint, request, jsonify
from app.common import cache, db
from app.models import User

BluePrint = Blueprint('app', __name__)


@BluePrint.route('/user/save', methods=['POST'])
def saveSnapshot():
    try:
        user_id = request.json.get("userId")
        user_name = request.json.get("userName")
        user_salary = request.json.get("userSalary")

        user = User(user_id, user_name, user_salary)
        db.session.add(user)
        db.session.commit()
        return jsonify(resultCode="0", resultMessage="SUCCESS", resultData=None)
    except:
        return jsonify(resultCode="-1", resultMessage="Interval Error!", resultData=None)


@BluePrint.route('/user/query', methods=['GET'])
def getCoefficients():
    try:
        user_id = request.args.get("userId")
        user = User.query.filter(User.user_id == user_id)
        # timeout为0表示永不过期
        cache.set(str(user_id), user, timeout=0)
        data = json.dumps(user.to_json())
        return jsonify(resultCode="0", resultMessage="SUCCESS", resultData=data)
    except:
        return jsonify(resultCode="-1", resultMessage="Interval Error!", resultData=None)


def sendDesire(data):
    url = "http://localhost:8080/recieveUser"
    headers = {"content-type": "application/json"}
    print('now is:', int(round(time.time() * 1000)))
    response = requests.request("POST", url, data=data, headers=headers)
    print(response)
