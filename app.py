import logging

from flask import Flask, jsonify, Response

from server import Server


def setup() -> None:
    logging.basicConfig(level = logging.INFO)


setup()
app = Flask(__name__)
server = Server()


@app.route('/candidate')
def get_candidate():
    return jsonify(server.get_candidate())


@app.route('/candidates')
def get_candidates():
    return jsonify(server.get_candidates())


@app.route('/invalidate')
def invalidate():
    server.invalidate()
    return app.response_class(response = None, status = 200)
