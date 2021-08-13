# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]
# Credits  : https://github.com/SpEcHiDe/AnyDLBot

import os
import threading
from sqlalchemy import create_engine
from sqlalchemy import Column, TEXT, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


def start() -> scoped_session:
    engine = create_engine(Config.DB_URI, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = threading.RLock()

class Ytdl(BASE):
    __tablename__ = "ytdl"
    id = Column(Numeric, primary_key=True)

    def __init__(self, id):
        self.id = id

Ytdl.__table__.create(checkfirst=True)


# ------------------------------------ Add user details ----------------------------- #
async def add_user(id):
    with INSERTION_LOCK:
        msg = SESSION.query(Ytdl).get(id)
        if not msg:
            usr = Ytdl(id)
            SESSION.add(usr)
            SESSION.commit()
        else:
            pass

async def query_msg():
    try:
        query = SESSION.query(Ytdl.id).order_by(Ytdl.id)
        return query
    finally:
        SESSION.close()
