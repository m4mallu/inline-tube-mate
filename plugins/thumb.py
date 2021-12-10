""" !/usr/bin/env python3
    -*- coding: utf-8 -*-
    Name     : inline-tube-mate [ Telegram ]
    Repo     : https://github.com/m4mallu/inine-tube-mate
    Author   : Renjith Mangal [ https://t.me/space4renjith ]
    Credits  : https://github.com/SpEcHiDe/AnyDLBot """

import os
from presets import Presets
from pyrogram.types import Message
from pyrogram import Client, filters
from support.buttons import reply_markup_thumb, reply_markup_close


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


@Client.on_message(filters.private & filters.photo)
async def save_photo(bot, m: Message):
    msg = await m.reply_text(Presets.WAIT_MESSAGE, reply_to_message_id=m.message_id)
    if m.from_user.id in Config.SUDO_USERS:
        await msg.edit(Presets.PROMPT_THUMB, reply_markup=reply_markup_thumb)
        return
    if Config.AUTH_USERS and (m.from_user.id not in Config.AUTH_USERS):
        await msg.edit_text(Presets.NOT_AUTH_TXT, reply_markup=reply_markup_close)
        return
    thumb_image = os.getcwd() + "/" + "thumbnails" + "/" + str(m.from_user.id) + ".jpg"
    await bot.download_media(m, thumb_image)
    await msg.edit_text(Presets.SAVED_THUMB, reply_markup=reply_markup_close)
