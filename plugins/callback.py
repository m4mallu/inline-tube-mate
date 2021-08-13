# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]
import asyncio
import os
from presets import Presets
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from library.display_progress import cancel_process
from plugins.youtube_dl_button import youtube_dl_call_back
from library.buttons import reply_markup_del_thumb, reply_markup_start, reply_markup_back, reply_markup_close


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


@Client.on_callback_query(filters.regex(r'^view_btn$'))
async def view_thumbnail(bot, cb: CallbackQuery):
    if Config.AUTH_USERS and (cb.from_user.id not in Config.AUTH_USERS):
        await cb.answer(Presets.NOT_AUTH_TXT, True)
        return
    thumb_image = os.getcwd() + "/" + "thumbnails" + "/" + str(cb.from_user.id) + ".jpg"
    if os.path.exists(thumb_image):
        await cb.message.delete()
        await bot.send_photo(
            cb.message.chat.id,
            thumb_image,
            Presets.THUMB_CAPTION,
            reply_markup=reply_markup_del_thumb
        )
    else:
        await cb.answer(Presets.NO_THUMB, True)


@Client.on_callback_query(filters.regex(r'^thumb_del_conf_btn$'))
async def delete_thumb(bot, cb: CallbackQuery):
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(cb.from_user.id) + ".jpg"
    try:
        os.remove(thumb_image_path)
    except Exception:
        pass
    await cb.answer(Presets.DEL_THUMB_CNF, True)
    await cb.message.delete()
    await cb.message.reply_text(Presets.OPTIONS_TXT,
                                reply_markup=reply_markup_start
                                )

@Client.on_callback_query(filters.regex(r'^a_back_btn$'))
async def a_back_button(bot, cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.reply_text(Presets.OPTIONS_TXT,
                                reply_markup=reply_markup_start
                                )

@Client.on_callback_query(filters.regex(r'^del_btn$'))
async def del_thumbnail(bot, cb: CallbackQuery):
    if Config.AUTH_USERS and (cb.from_user.id not in Config.AUTH_USERS):
        await cb.answer(Presets.NOT_AUTH_TXT, True)
        return
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(cb.from_user.id) + ".jpg"
    if os.path.exists(thumb_image_path):
        try:
            os.remove(thumb_image_path)
        except Exception:
            pass
        await cb.answer(Presets.DEL_THUMB_CNF, True)
    else:
        await cb.answer(Presets.NO_THUMB, True)


@Client.on_callback_query(filters.regex(r'^help_btn$'))
async def help_bot(bot, cb: CallbackQuery):
    await cb.answer()
    await cb.message.edit_text(Presets.HELP_TEXT,
                               disable_web_page_preview=True,
                               reply_markup=reply_markup_back
                               )


@Client.on_callback_query(filters.regex(r'^back_btn$'))
async def back_button(bot, cb: CallbackQuery):
    await cb.message.edit_text(Presets.OPTIONS_TXT,
                               reply_markup=reply_markup_start
                               )


@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def clos_button(bot, cb: CallbackQuery):
    try:
        await cb.message.delete()
    except Exception:
        pass


@Client.on_callback_query(filters.regex(r'^home_btn$'))
async def home_button(bot, cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.reply_text(Presets.OPTIONS_TXT,
                                reply_markup=reply_markup_start
                                )


@Client.on_callback_query(filters.regex(r'^cancel_btn$'))
async def cancel_upload_process(bot, cb: CallbackQuery):
    id = int(cb.from_user.id)
    cancel_process.pop(id)
    await cb.message.edit_text(Presets.CANCEL_PROCESS)
    await asyncio.sleep(5)
    await cb.message.delete()


@Client.on_callback_query(filters.regex(r'^set_thumb_btn$'))
async def set_thumb(bot, cb: CallbackQuery):
    await cb.message.edit(Presets.DOWNLOAD_START)
    thumb_image = os.getcwd() + "/" + "thumbnails" + "/" + str(cb.from_user.id) + ".jpg"
    message = cb.message.reply_to_message
    await bot.download_media(message, thumb_image)
    await cb.message.edit_text(Presets.SAVED_THUMB, reply_markup=reply_markup_close)


@Client.on_callback_query()
async def Youtube_dl_button(bot, cb: CallbackQuery):
    if "|" in cb.data:
        await youtube_dl_call_back(bot, cb)
        await youtube_dl_call_back(bot, cb)
