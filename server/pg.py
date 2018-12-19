#!/usr/bin/python3
# vim: ts=4 sts=4 sw=4 et smartindent

import psycopg2, psycopg2.extras
import json, datetime, binascii
from ..common.data import *

PGPORT=5433
DEBUG_PRINT=False

def _Connect():
    conn = psycopg2.connect(
            dbname="taskmaster", port=PGPORT,
            cursor_factory=psycopg2.extras.DictCursor)
    return conn

class EntityNotFoundException(Exception):
    pass

def Query(sql, params=()):
    params = _FixParams(params)
    conn = _Connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        if DEBUG_PRINT:
            print(cur.query)
            print(cur.statusmessage)
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
        if DEBUG_PRINT:
            print(cur.query)
            print(cur.statusmessage)
        row = cur.fetchone()
        cur.close()
        if row == None:
            raise EntityNotFoundException(sql, params)
        return row
    finally:
        conn.close()

def Insert(tableName, colVals):
    cols = [ cv[0] for cv in colVals ]
    vals = [ cv[1] for cv in colVals ]
    sql = 'insert into %s (%s) values (%s)' % (
        tableName, ', '.join(cols),
        ', '.join('%s' for x in range(len(vals)))
    )
    #print(sql + ' -- ' + '; '.join((str(v) for v in vals)))
    conn = _Connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, vals)
        if DEBUG_PRINT:
            print(cur.query)
            print(cur.statusmessage)
        rowcount = cur.rowcount
        cur.close()
        conn.commit()
        return rowcount
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

class _JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat(' ')[:19]
        return json.JSONEncoder.default(self, o)

def ToJson(x):
    j = json.dumps(x, cls=_JSONEncoder)
    return j

if __name__ == "__main__":
    DEBUG_PRINT=True
    r = Query("select * from usr")
    j = ToJson(ResultsToDicts(r))
    print(j)
    r = Query1("select * from tsk limit 1")
    j = ToJson(ResultToDict(r))
    print(j)
    rc = Insert('usr', (('username', 'msa'), ('fullname', 'Marison A'),))
    print("Insert usr OK: %d rows affected" % rc)
    r = Query("select * from usr")
    j = ToJson(ResultsToDicts(r))
    print(j)

