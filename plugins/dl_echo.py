""" !/usr/bin/env python3
    -*- coding: utf-8 -*-
    Name     : inline-tube-mate [ Telegram ]
    Repo     : https://github.com/m4mallu/inine-tube-mate
    Author   : Renjith Mangal [ https://t.me/space4renjith ]
    Credits  : https://github.com/SpEcHiDe/AnyDLBot """

import os
import json
import asyncio
from presets import Presets
from pytube import YouTube as ytdl
from pyrogram import Client, filters
from support.progress import humanbytes
from support.extract import yt_link_search, yt_thumb_dl
from support.buttons import reply_markup_close, get_chat_invite_link, get_public_chat_link
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputMediaPhoto


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


xxx = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(filters.private & filters.regex(xxx))
async def echo(bot, m: Message):
    img = await m.reply_photo(Presets.INITIAL_MEDIA, quote=True)
    # If the Authorized user list is present, then only allow the above users to download videos. Else, will allow all.
    if Config.AUTH_USERS and (m.from_user.id not in Config.AUTH_USERS):
        await img.edit_media(
            InputMediaPhoto(media=Presets.ERROR_MEDIA, caption=Presets.NOT_AUTH_TXT),
            reply_markup=reply_markup_close
        )
        return
    # Force a subscriber to join a specific chat [ It happens only when Authorized users list is empty]
    if (not Config.AUTH_USERS) and Config.FORCE_SUB_CHAT:
        chat = []
        me = await bot.get_me()
        # Checking, the bot is already in the chat or not.
        try:
            await bot.get_chat_member(int(Config.FORCE_SUB_CHAT), me.username)
        except Exception:
            await img.edit_media(
                InputMediaPhoto(media=Presets.ERROR_MEDIA, caption=Presets.BOT_NOT_PRESENT),
                reply_markup=reply_markup_close
            )
            return
        # Checking, the user is already in the chat or not. Also collecting the chat parameters.
        try:
            chat = await bot.get_chat(int(Config.FORCE_SUB_CHAT))
            await bot.get_chat_member(int(Config.FORCE_SUB_CHAT), m.from_user.username)
        except Exception:
            # If the user is not in the chat, then force him to join the chat.
            # For public chats.
            if chat.username:
                await img.edit_media(
                    InputMediaPhoto(media=Presets.ERROR_MEDIA, caption=Presets.NOT_SUB_TXT),
                    reply_markup=get_public_chat_link(chat.username)
                )
                return
            # For private chats
            elif chat.invite_link:
                await img.edit_media(
                    InputMediaPhoto(media=Presets.ERROR_MEDIA, caption=Presets.NOT_SUB_TXT),
                    reply_markup=get_chat_invite_link(chat.invite_link)
                )
                return
            else:
                # If an invite link is not found, then throw a message to create an invite link.
                await img.edit_media(
                    InputMediaPhoto(media=Presets.ERROR_MEDIA, caption=Presets.NO_INVITE_METHOD),
                    reply_markup=reply_markup_close
                )
                return
    else:
        pass
    yt = ytdl(m.text)
    url = yt.watch_url
    thumb_url = yt.thumbnail_url
    command_to_exec = [
        "youtube-dl",
        "--no-warnings",
        "--youtube-skip-dash-manifest",
        "-j",
        url
    ]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if e_response and "nonnumeric port" not in e_response:
        error_message = e_response.replace(Presets.AD_STRING_TO_REPLACE, "")
        if "This video is only available for registered users." in error_message:
            error_message += Presets.SET_CUSTOM_USERNAME_PASSWORD
        await bot.send_message(
            chat_id=m.chat.id,
            text=Presets.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            reply_to_message_id=m.message_id,
            parse_mode="html",
            disable_web_page_preview=True
        )
        return False
    if t_response:
        x_reponse = t_response
        if "\n" in x_reponse:
            x_reponse, _ = x_reponse.split("\n")
        response_json = json.loads(x_reponse)
        json_path = os.getcwd() + "/" + "downloads"
        if not os.path.isdir(json_path):
            os.makedirs(json_path)
        save_ytdl_json_path = json_path + "/" + str(m.from_user.id) + ".json"
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        inline_keyboard = []
        duration = None
        if "duration" in response_json:
            duration = response_json["duration"]
        if "formats" in response_json:
            for formats in response_json["formats"]:
                format_id = formats.get("format_id")
                format_string = formats.get("format_note")
                if format_string is None:
                    format_string = formats.get("format")
                format_ext = formats.get("ext")
                approx_file_size = ""
                if "filesize" in formats:
                    approx_file_size = humanbytes(formats["filesize"])
                cb_string_video = "{}|{}|{}".format(
                    "video", format_id, format_ext)
                cb_string_file = "{}|{}|{}".format(
                    "file", format_id, format_ext)
                if format_string is not None and not "audio only" in format_string:
                    ikeyboard = [
                        InlineKeyboardButton(
                            "S " + format_string + " video " + approx_file_size + " ",
                            callback_data=cb_string_video.encode("UTF-8")
                        ),
                        InlineKeyboardButton(
                            "D " + format_ext + " " + approx_file_size + " ",
                            callback_data=cb_string_file.encode("UTF-8")
                        )
                    ]
                else:
                    ikeyboard = [
                        InlineKeyboardButton(
                            "SVideo [" +
                            "] ( " +
                            approx_file_size + " )",
                            callback_data=cb_string_video.encode("UTF-8")
                        ),
                        InlineKeyboardButton(
                            "DFile [" +
                            "] ( " +
                            approx_file_size + " )",
                            callback_data=cb_string_file.encode("UTF-8")
                        )
                    ]
                inline_keyboard.append(ikeyboard)
            if duration is not None:
                cb_string_64 = "{}|{}|{}".format("audio", "64k", "mp3")
                cb_string_128 = "{}|{}|{}".format("audio", "128k", "mp3")
                cb_string = "{}|{}|{}".format("audio", "320k", "mp3")
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "🎶MP3🎶" + "(" + "64 kbps" + ")", callback_data=cb_string_64.encode("UTF-8")),
                    InlineKeyboardButton(
                        "🎶MP3🎶 " + "(" + "128 kbps" + ")", callback_data=cb_string_128.encode("UTF-8"))
                ])
                inline_keyboard.append([
                    InlineKeyboardButton(
                        "🎶MP3🎶 " + "(" + "320 kbps" + ")", callback_data=cb_string.encode("UTF-8"))
                ])
        else:
            format_id = response_json["format_id"]
            format_ext = response_json["ext"]
            cb_string_file = "{}|{}|{}".format(
                "file", format_id, format_ext)
            cb_string_video = "{}|{}|{}".format(
                "video", format_id, format_ext)
            inline_keyboard.append([
                InlineKeyboardButton(
                    "🎞️SVideo🎞️",
                    callback_data=cb_string_video.encode("UTF-8")
                ),
                InlineKeyboardButton(
                    "🗂️DFile🗂️",
                    callback_data=cb_string_file.encode("UTF-8")
                )
            ])
            cb_string_file = "{}={}={}".format(
                "file", format_id, format_ext)
            cb_string_video = "{}={}={}".format(
                "video", format_id, format_ext)
            inline_keyboard.append([
                InlineKeyboardButton(
                    "video",
                    callback_data=cb_string_video.encode("UTF-8")
                ),
                InlineKeyboardButton(
                    "file",
                    callback_data=cb_string_file.encode("UTF-8")
                )
            ])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        # Fetching YouTube url details
        try:
            result = await yt_link_search(url)
            views = result['viewCount']['text']
            title = result['title'][:25] + ".."
            link = result['channel']['link']
            channel = result['channel']['name']
            rating = round(result['averageRating'], 1) if result['averageRating'] else "N/A"
            uploaded_date = result['uploadDate']
            thumb = await yt_thumb_dl(thumb_url, m)
        except Exception:
            await img.edit_caption(Presets.NOT_DOWNLOADABLE)
            await asyncio.sleep(5)
            await img.delete()
            return
        await img.edit_media(
            InputMediaPhoto(
                media=thumb,
                caption=Presets.FORMAT_SELECTION.format(
                    title,
                    link,
                    channel,
                    uploaded_date,
                    views,
                    rating
                )
            ),
            reply_markup=reply_markup
        )
