#  sqlite_helper.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2023.
#
# https://docs.python.org/3/library/sqlite3.html#sqlite3-controlling-transactions
# https://github.com/python/cpython/blob/main/Lib/sqlite3/__main__.py
# https://github.com/python/cpython/tree/main/Modules/_sqlite
# https://www.sqlite.org/datatype3.html

import sqlite3

__all__ = ["sqlite_connection",
           "sqlite_execute",
           "sqlite_executemany",
           "sqlite_executescript",
           "sqlite_fetchone",
           "sqlite_fetchmany",
           "sqlite_fetchall"]


def sqlite_connection(dest: str = None, is_row: bool = False) -> sqlite3.Connection:
    """커넥션 반환. is_row 가 True 이면 반환값으로 sqlite3.Row 객체를 준다."""
    conn = sqlite3.connect(dest if dest else ':memory:')
    if is_row:
        conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def sqlite_execute(dest: str, query: str, params=()):
    """한 트랜젝션에서 오직 하나의 쿼리만 수행"""
    conn = sqlite_connection(dest)
    cur = conn.cursor()
    try:
        cur.execute(query, params)
    except sqlite3.Connection.Error as error:
        conn.rollback()
        raise error
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()


def sqlite_executemany(dest: str, query: str, params=()):
    """한 트랜젝션에서 하나의 커리를 여러 번 수행"""
    conn = sqlite_connection(dest)
    cur = conn.cursor()
    try:
        cur.executemany(query, params)
    except sqlite3.Connection.Error as error:
        conn.rollback()
        raise error
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()


def sqlite_executescript(dest: str, script: str):
    """한 트랜젝션에서 여러 쿼리를 처리하려고 할 때 사용. 매개변수 없으니 쿼리문을 완성해서 넘겨라."""
    conn = sqlite_connection(dest)
    cur = conn.cursor()
    try:
        cur.executescript(script)
    except Exception as error:
        conn.rollback()
        raise error
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()


def sqlite_fetchone(dest: str, query: str, params=()) -> tuple:
    """아이템 하나당 튜플이며, 튜플 단품으로 반환된다."""
    with sqlite_connection(dest) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchone()
        cur.close()
    return rows


def sqlite_fetchmany(dest: str, query: str, size=1, params=()) -> list[tuple]:
    """아이템 하나당 튜플이며, 튜플이 담긴 리스트로 반환된다."""
    with sqlite_connection(dest) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchmany(size)
        cur.close()
    return rows


def sqlite_fetchall(dest: str, query: str, params=()) -> list[tuple]:
    """아이템 하나당 튜플이며, 튜플이 담긴 리스트로 반환된다."""
    with sqlite_connection(dest) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
    return rows
