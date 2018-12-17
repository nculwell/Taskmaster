#!/usr/bin/python3
# vim: ts=4 sts=4 sw=4 et smartindent

import psycopg2, psycopg2.extras
import json, datetime

PGPORT=5433

def _Connect():
    conn = psycopg2.connect(
            dbname="taskmaster", port=PGPORT,
            cursor_factory=psycopg2.extras.DictCursor)
    return conn

def Query(sql, params=()):
    params = _FixParams(params)
    conn = _Connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        rowCount = cur.rowcount
        cur.close()
        return rows
    finally:
        conn.close()

def Query1(sql, params=()):
    params = _FixParams(params)
    conn = _Connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        return row
    finally:
        conn.close()

def ResultToDict(result):
    return { k: v for k, v in result.items() }

def ResultsToDicts(results):
    return [ ResultToDict(r) for r in results ]

def _FixParams(params):
    if isinstance(params, list) or isinstance(params, tuple):
        return params
    return (params,)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat(' ')[:19]
        return json.JSONEncoder.default(self, o)

if __name__ == "__main__":
    r = Query("select * from usr")
    j = json.dumps(ResultsToDicts(r), cls=JSONEncoder)
    print(j)

