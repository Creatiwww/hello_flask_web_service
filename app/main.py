from flask import Flask, jsonify, make_response
from werkzeug.contrib.fixers import ProxyFix
import requests

import database as db

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

robot_ip = 'http://192.168.88.198'
robot_url = robot_ip
requests2robot_timeout = 10

api_base = '/robot/api/v1.0'


# check weather the Server is alive
@app.route(api_base + '/ping/server', methods=['GET'])
def ping_server():
    return jsonify(
        {
            'web_server_response': 'Server is running...'
        })


# check weather the Robot is alive
@app.route(api_base + '/ping/robot', methods=['GET'])
def ping_robot():
    # TODO implement exception - In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception
    r = requests.get(robot_url + '/ping', timeout=requests2robot_timeout)
    if r.status_code == requests.codes.ok:
        json_response = jsonify(
            {
                'web_server_response': r.text
            })
    else:
        json_response = jsonify(
            {
                'web_server_response': r.status_code
            })
    return json_response


# interface for robot movement control
@app.route(api_base + '/control/<command>', methods=['GET'])
def control(command):
    r = requests.get(robot_url + '/control/' + command, timeout=requests2robot_timeout)
    if r.status_code == requests.codes.ok:
        json_response = jsonify(
            {
                'web_server_response': r.text
            })
    else:
        json_response = jsonify(
            {
                'web_server_response': r.status_code
            })
    return json_response


# interface for requesting distance from robot
@app.route(api_base + '/sensor/d', methods=['GET'])
def request_distance():
    r = requests.get(robot_url + "/sensor/d", timeout=requests2robot_timeout)
    if r.status_code == requests.codes.ok:

        # getting целую часть от расстояния в формате int
        distance_str_in = r.json()['distance']
        point_pos = distance_str_in.find('.')
        distance_str_out = distance_str_in[:point_pos]
        distance_int = distance_str_out

        json_response = jsonify(
            {
                "distance": distance_int
            })

        # adding record to database
        db.add(distance_value=distance_int)
    else:
        json_response = jsonify(
            {
                'web_server_response': r.status_code
            })
    return json_response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(
        {
            'web_server_response': 'error: call is not correct'
        }), 404)


@app.route("/initdb")
def init_db():
    return db.init_db()


@app.route("/getall/d")
def get_all_distances():
    return db.get_all_d()
