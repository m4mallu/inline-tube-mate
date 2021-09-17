# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]
# Credits  : https://github.com/SpEcHiDe/AnyDLBot


import os
import re
import wget
import json
import asyncio
from presets import Presets
from pyrogram import Client, filters
from library.extract import yt_link_search
from library.display_progress import humanbytes
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(filters.private & filters.regex(ytregex))
async def echo(bot, m: Message):
    if Config.AUTH_USERS and (m.from_user.id not in Config.AUTH_USERS):
        await m.reply_text(Presets.NOT_AUTH_TXT, reply_to_message_id=m.message_id)
        return
    msg = await m.reply_text(text=Presets.CHECKING_LINK, quote=True)
    url = m.text
    youtube_dl_username = None
    youtube_dl_password = None
    file_name = None
    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in m.entities:
                if entity.type == "text_link":
                    url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    ln = entity.length
                    url = url[o:o + ln]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
    else:
        for entity in m.entities:
            if entity.type == "text_link":
                url = entity.url
            elif entity.type == "url":
                o = entity.offset
                ln = entity.length
                url = url[o:o + ln]
    if Config.HTTP_PROXY != "":
        command_to_exec = [
            "youtube-dl",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url,
            "--proxy", Config.HTTP_PROXY
        ]
    else:
        command_to_exec = [
            "youtube-dl",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "-j",
            url
        ]
    if "hotstar" in url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
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
        yt_thumb_image_path = os.getcwd() + "/" + "YThumb" + "/" + str(m.from_user.id) + ".jpg"
        yt_thumb_dir = os.getcwd() + "/" + "YThumb" + "/"
        if not os.path.isdir(yt_thumb_dir):
            os.makedirs(yt_thumb_dir)
        else:
            try:
                os.remove(yt_thumb_image_path)
            except Exception:
                pass
        try:
            result = await yt_link_search(url)
            views = result['viewCount']['text']
            title = result['title'][:25] + ".."
            link = result['channel']['link']
            channel = result['channel']['name']
            rating = round(result['averageRating'], 1)
            uploaded_date = result['uploadDate']
            exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
            sx = re.findall(exp, url)[0][-1]
            thumb = f"https://i.ytimg.com/vi/{sx}/maxresdefault.jpg"
            wget.download(thumb, yt_thumb_image_path, bar=None)
        except Exception:
            await msg.edit(Presets.NOT_DOWNLOADABLE)
            await m.delete()
            await asyncio.sleep(5)
            await msg.delete()
            return
        await msg.delete()
        await m.reply_photo(photo=thumb,
                            caption=Presets.FORMAT_SELECTION.format(title,
                                                                    link,
                                                                    channel,
                                                                    uploaded_date,
                                                                    views,
                                                                    rating
                                                                    ),
                            reply_to_message_id=m.message_id,
                            reply_markup=reply_markup,
                            parse_mode='html'
                            )
