import threading

from flask import Flask, jsonify, request

from cache.cachedpool import CachedPool
from candidates.client.impl.parsingcandidatesclient import ParsingCandidatesClient
from candidates.parser.impl.freeproxylist import FreeProxyListParser
from log.log import Log
from scheduler.scheduler import Scheduler

Log.init()

scheduler = Scheduler().start()

client = ParsingCandidatesClient(
    source = 'https://free-proxy-list.net',
    parser = FreeProxyListParser)

candidate_pool = (CachedPool()
                  .cache_provider(client.get_candidates)
                  .schedule_rebuild(lambda rebuild: scheduler.interval(60 * 30, rebuild)))

app = Flask(__name__)


@app.route('/get', methods = ['GET'])
def get_candidates():
    count = int(request.args.get('count'))
    return jsonify([candidate.to_json() for candidate in candidate_pool.get_next(count)])


@app.route('/invalidate')
def invalidate():
    candidate_pool.schedule_rebuild(lambda rebuild: threading
                                    .Thread(target = rebuild, daemon = True)
                                    .start())

    return app.response_class(
        response = None,
        status = 200
    )
