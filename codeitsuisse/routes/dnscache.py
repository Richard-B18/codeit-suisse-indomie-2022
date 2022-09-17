from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import json
from codeitsuisse import app

import logging
logger = logging.getLogger(__name__)


class LRUCache:
    def __init__(self, capacity: int):
        self.hashmap = {}
        self.cap = capacity
        self.elementsSoFar = 0
        self.hashqueue = {}

    def get(self, key: int) -> int:
        if key in self.hashmap:
            self.hashqueue.pop(key)
            self.hashqueue[key] = None
            return self.hashmap[key]
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key not in self.hashmap:
            self.elementsSoFar += 1
        self.hashmap[key] = value
        self.hashqueue[key] = None
        if self.elementsSoFar > self.cap:
            toRemove = next(iter(self.hashqueue))   # key to remove
            self.hashqueue.pop(toRemove)
            self.hashmap.pop(toRemove)
            self.elementsSoFar -= 1
        else:
            self.hashqueue.pop(key)
            self.hashqueue[key] = None
        # print(self.hashmap)
        # print(self.hashqueue)
        return

@app.route('/instantiateDNSLookup', methods=["POST"])
def solve():
    db = TinyDB('db.json')
    data = request.get_json()
    logger.info(data)
    for domain in data["lookupTable"]:
        db.insert({ 'domain' : domain, 'ip' : data["lookupTable"][domain] })
    toReturn = {
        "success": True
    }
    return json.dumps(toReturn)

@app.route('/simulateQuery', methods=["POST"])
def stimulate():
    db = TinyDB('db.json')
    Mapping = Query()
    data = request.get_json()
    cache = LRUCache(data["cacheSize"])
    resultArr = []
    for domain in data["log"]:
        returnObj = {
            "status": None, "ipAddress": None
        }
        if cache.get(domain) == -1:
            returnObj["status"] = "cache miss"
            queryList = db.search(Mapping.domain == domain)
            if not queryList:
                returnObj["status"] = "invalid"
            else:
                pair = queryList[0]
                returnObj["ipAddress"] = pair["ip"]
                cache.put(domain, pair["ip"])
        else:
            returnObj["status"] = "cache hit"
            returnObj["ipAddress"] = cache.get(domain)
        resultArr.append(returnObj)
    return jsonify(resultArr)