# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]

import os
import asyncio
from presets import Presets
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from library.support import users_info
from library.sql import add_user, query_msg
from library.buttons import reply_markup_start, reply_markup_close


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


@Client.on_message(filters.private & filters.command(['start', 'help']))
async def start_bot(bot, m: Message):
    await add_user(m.from_user.id)
    await m.reply_text(Presets.WELCOME_MSG.format(m.from_user.first_name),
                       reply_markup=reply_markup_start)


@Client.on_message(filters.private & filters.command('send'))
async def send_messages(bot, m: Message):
    if m.from_user.id not in Config.SUDO_USERS:
        return
    await m.delete()
    if m.reply_to_message is not None:
        msg = await m.reply_text(Presets.SEND_TEXT)
        query = await query_msg()
        for row in query:
            chat_id = int(row[0])
            try:
                await bot.copy_message(
                    chat_id=chat_id,
                    from_chat_id=m.chat.id,
                    message_id=m.reply_to_message.message_id,
                    caption=m.caption
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception:
                pass
        await msg.delete()
    else:
        await m.delete()
        await m.reply_text(Presets.REPLY_ERROR,
                           m.message_id,
                           reply_markup=reply_markup_close
                           )


@Client.on_message(filters.private & filters.command('subs'))
async def subscribers_count(bot, m: Message):
    id = m.from_user.id
    if id not in Config.SUDO_USERS:
        return
    msg = await m.reply_text(Presets.WAIT_MSG)
    await m.delete()
    messages = await users_info(bot)
    active = messages[0]
    blocked = messages[1]
    total = active + blocked
    await msg.edit(Presets.USERS_LIST.format(total, active, blocked),
                   reply_markup=reply_markup_close)
