#  db_store.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

import os
from typing import NamedTuple, Iterable
from util.sqlite_helper import *


class DBStore:
    def __init__(self, db: str, schema: str):
        self.db = db
        self.schema = schema
        if not os.path.exists(db):
            with open(schema, encoding='UTF8') as s:
                sqlite_executescript(db, s.read())

    def clear_human(self, is_table=False):
        query = r"""DROP TABLE IF EXISTS human;"""
        if is_table:
            sqlite_execute(dest=self.db, query=query)
        else:
            # SQLite 는 TRUNCATE 가 없어. 그래서.. 드랍시키고 다시 생성.
            with open(self.schema, encoding='UTF8') as s:
                sqlite_executescript(self.db, query + s.read())

    def count_human(self) -> int:
        query = r"""SELECT COUNT(*) FROM human;"""
        return sqlite_fetchone(self.db, query)[0]

    def create_human(self, hus: 'DB.Human' | Iterable['DB.Human']):
        query = r"""INSERT OR IGNORE
                    INTO human
                    VALUES (?,?,?,?,?,?,?,?,?);"""
        if isinstance(hus, DB.Human):
            sqlite_execute(self.db, query, hus)
        else:
            # 배열에 담긴 휴먼으로 추정하고 many 로 돌린다.
            sqlite_executemany(self.db, query, hus)

    def read_human(self, uid: str):
        query = r"""SELECT * 
                    FROM human 
                    WHERE id=?
                    LIMIT 1;"""
        row = sqlite_fetchone(self.db, query, (uid,))
        return DB.Human(*row)

    def read_human_meta(self, uid: str):
        query = r"""SELECT id, name, age, country 
                    FROM human 
                    WHERE id=?
                    LIMIT 1;"""
        row = sqlite_fetchone(self.db, query, (uid,))
        return DB.Human.Meta(*row)

    def read_human_meta_all(self, size=100):
        query = r"""SELECT id, name, age, country 
                    FROM human;"""
        rows = sqlite_fetchmany(dest=self.db, query=query, size=size)
        return [DB.Human.Meta(*row) for row in rows]

    def update_human_meta(self, hum: 'DB.Human.Meta'):
        query = r"""UPDATE human
                    SET name=?, age=?, country=?
                    WHERE id=?;"""
        sqlite_execute(dest=self.db, query=query, params=(hum.name, hum.age, hum.country, hum.uid))

    def delete_human(self, uid: str):
        query = r"""DELETE FROM human
                    WHERE id=?;"""
        sqlite_execute(dest=self.db, query=query, params=(uid,))


class DB:
    class Human(NamedTuple):
        uid: str
        name: str
        username: str
        gender: str
        email: str
        age: int
        country: str
        cellphone: str = None
        photo: str = None

        class Meta(NamedTuple):
            uid: str
            name: str
            age: int
            country: str
