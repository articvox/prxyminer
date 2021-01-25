import logging

from flask import Flask, jsonify, request

from cachedpool import CachedPool
from candidates.client.impl.parsingcandidatesclient import ParsingCandidatesClient
from candidates.parser.impl.freeproxylist import FreeProxyListParser
from log import Log
from scheduler import Scheduler

Log.init()

candidates = CachedPool(data_src = ParsingCandidatesClient(source = 'https://free-proxy-list.net',
                                                           parser = FreeProxyListParser).get_candidates,
                        scheduler = Scheduler().start())

app = Flask(__name__)


@app.route('/get', methods = ['GET'])
def get_candidates():
    return jsonify([candidate.to_json() for candidate in candidates.get_n_pooled(request.args.get('count'))])


@app.route('/invalidate')
def invalidate():
    candidates.invalidate()
    return app.response_class(response = None, status = 200)
