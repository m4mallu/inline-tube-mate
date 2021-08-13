# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]

import os
import asyncio
from pyrogram import Client
from presets import Presets
from library.sql import add_user
from library.info import get_info
from pyrogram.errors import FloodWait
from library.extract import youtube_search
from pyrogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


@Client.on_inline_query()
async def inline_search(bot, query: InlineQuery):
    await add_user(query.from_user.id)
    me = []
    try:
        me = await Client.get_me(bot)
    except FloodWait as e:
        await asyncio.sleep(e.x)
    id = query.from_user.id
    results = []
    #
    defaults = await get_info(me.username)
    results.extend(defaults)
    #
    try:
        if Config.AUTH_USERS and (id not in Config.AUTH_USERS):
            await query.answer(results=results,
                               switch_pm_text=Presets.NOT_AUTH_TXT,
                               switch_pm_parameter="help"
                               )
            return
    except FloodWait as e:
        await asyncio.sleep(e.x)
    #
    search = query.query.strip()
    string = await youtube_search(search)
    for data in string:
        count = data['viewCount']
        thumb = data['thumbnails']
        results.append(
            InlineQueryResultArticle(
                title=data['title'][:35] + "..",
                input_message_content=InputTextMessageContent(
                    message_text=data['link']
                ),
                thumb_url=thumb[0]['url'],
                description=Presets.DESCRIPTION.format(data['duration'], count['text'])
            )
        )
    if string:
        switch_pm_text = Presets.RESULTS_TXT
        try:
            await query.answer(
                results=results,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start"
            )
        except Exception:
            pass
    else:
        switch_pm_text = Presets.NO_RESULTS
        try:
            await query.answer(
                results=results,
                switch_pm_text=switch_pm_text,
                switch_pm_parameter="start"
            )
        except Exception:
            pass
