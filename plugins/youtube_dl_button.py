# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]
# Credits  : https://github.com/SpEcHiDe/AnyDLBot


import os
import time
import json
import shutil
import asyncio
from presets import Presets
from datetime import datetime
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from library.buttons import reply_markup_cancel
from library.display_progress import cancel_process
from library.buttons import reply_markup_join, reply_markup_close
from library.display_progress import progress_for_pyrogram, humanbytes


if bool(os.environ.get("ENV", False)):
    from sample_config import Config
else:
    from config import Config


async def youtube_dl_call_back(bot, m):
    id = int(m.from_user.id)
    cancel_process[id] = int(m.message.message_id)
    cb_data = m.data
    tg_send_type, youtube_dl_format, youtube_dl_ext = cb_data.split("|")
    thumb_image_path = os.getcwd() + "/" + "thumbnails" + "/" + str(m.from_user.id) + ".jpg"
    yt_thumb_image_path = os.getcwd() + "/" + "YThumb" + "/" + str(m.from_user.id) + ".jpg"
    save_ytdl_json_path = os.getcwd() + "/" + "downloads" + "/" + str(m.from_user.id) + ".json"
    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except FileNotFoundError as e:
        await bot.delete_messages(
            chat_id=m.message.chat.id,
            message_ids=m.message.message_id,
            revoke=True
        )
        return False
    youtube_dl_url = m.message.reply_to_message.text
    custom_file_name = str(response_json.get("title")) + "_" + youtube_dl_format + "." + youtube_dl_ext
    thumb_nail = None
    youtube_dl_username = None
    youtube_dl_password = None
    if "|" in youtube_dl_url:
        url_parts = youtube_dl_url.split("|")
        if len(url_parts) == 2:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
        elif len(url_parts) == 4:
            youtube_dl_url = url_parts[0]
            custom_file_name = url_parts[1]
            youtube_dl_username = url_parts[2]
            youtube_dl_password = url_parts[3]
        else:
            for entity in m.message.reply_to_message.entities:
                if entity.type == "text_link":
                    youtube_dl_url = entity.url
                elif entity.type == "url":
                    o = entity.offset
                    ln = entity.length
                    youtube_dl_url = youtube_dl_url[o:o + ln]
        if youtube_dl_url is not None:
            youtube_dl_url = youtube_dl_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        if youtube_dl_username is not None:
            youtube_dl_username = youtube_dl_username.strip()
        if youtube_dl_password is not None:
            youtube_dl_password = youtube_dl_password.strip()
    else:
        for entity in m.message.reply_to_message.entities:
            if entity.type == "text_link":
                youtube_dl_url = entity.url
            elif entity.type == "url":
                o = entity.offset
                ln = entity.length
                youtube_dl_url = youtube_dl_url[o:o + ln]
    try:
        await bot.edit_message_text(
            text=Presets.DOWNLOAD_START,
            chat_id=m.message.chat.id,
            message_id=m.message.message_id
        )
    except Exception:
        pass
    description = Presets.CUSTOM_CAPTION_UL_FILE
    if "fulltitle" in response_json:
        description = Presets.CUSTOM_CAPTION_UL_FILE.format(response_json["fulltitle"][0:1021])
    tmp_directory_for_each_user = os.getcwd() + "/" + "downloads" + "/" + str(m.from_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = tmp_directory_for_each_user + "/" + custom_file_name
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "youtube-dl",
            "-c",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--prefer-ffmpeg",
            "--extract-audio",
            "--audio-format", youtube_dl_ext,
            "--audio-quality", youtube_dl_format,
            youtube_dl_url,
            "-o", download_directory
        ]
    else:
        minus_f_format = youtube_dl_format
        if "youtu" in youtube_dl_url:
            minus_f_format = youtube_dl_format + "+bestaudio"
        command_to_exec = [
            "youtube-dl",
            "-c",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--embed-subs",
            "-f", minus_f_format,
            "--hls-prefer-ffmpeg", youtube_dl_url,
            "-o", download_directory
        ]
    if Config.HTTP_PROXY != "":
        command_to_exec.append("--proxy")
        command_to_exec.append(Config.HTTP_PROXY)
    if youtube_dl_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(youtube_dl_username)
    if youtube_dl_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(youtube_dl_password)
    command_to_exec.append("--no-warnings")
    if "hotstar" in youtube_dl_url:
        command_to_exec.append("--geo-bypass-country")
        command_to_exec.append("IN")

    start = datetime.now()
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    ad_string_to_replace = Presets.AD_STRING_TO_REPLACE
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await bot.edit_message_text(
            chat_id=m.message.chat.id,
            message_id=m.message.message_id,
            text=error_message
        )
        return False
    if t_response:
        try:
            os.remove(save_ytdl_json_path)
        except Exception:
            pass
        file_size = Config.TG_MAX_FILE_SIZE + 1
        try:
            file_size = os.stat(download_directory).st_size
        except FileNotFoundError as exc:
            try:
                download_directory = os.path.splitext(download_directory)[0] + "." + "mkv"
                file_size = os.stat(download_directory).st_size
            except Exception:
                await bot.edit_message_text(
                    chat_id=m.message.chat.id,
                    text=Presets.LINK_ERROR,
                    message_id=m.message.message_id,
                    reply_markup=reply_markup_close
                )
                return
        if file_size > Config.TG_MAX_FILE_SIZE:
            await bot.edit_message_text(
                chat_id=m.message.chat.id,
                text=Presets.RCHD_TG_API_LIMIT.format(humanbytes(file_size)),
                message_id=m.message.message_id
            )
        else:
            try:
                await bot.edit_message_text(text=Presets.UPLOAD_START,
                                            chat_id=m.message.chat.id,
                                            message_id=m.message.message_id,
                                            reply_markup=reply_markup_cancel
                                            )
            except Exception:
                pass
            # get the correct width, height, and duration for videos greater than 10MB
            metadata = extractMetadata(createParser(download_directory))
            duration = 0
            if tg_send_type != "file":
                if metadata is not None:
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
            if os.path.exists(thumb_image_path):
                thumb_nail = thumb_image_path
            elif (not os.path.exists(thumb_image_path)) and (os.path.exists(yt_thumb_image_path)):
                thumb_nail = yt_thumb_image_path
            else:
                thumbnails = None
            start_time = time.time()
            if id in cancel_process:
                if tg_send_type == "audio":
                    await m.message.reply_to_message.reply_chat_action("upload_audio")
                    await bot.send_audio(
                        chat_id=m.message.chat.id,
                        audio=download_directory,
                        caption=description,
                        duration=duration,
                        parse_mode="HTML",
                        thumb=thumb_nail,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Presets.UPLOAD_START,
                            m.message,
                            start_time,
                            bot,
                            id
                        )
                    )
                elif tg_send_type == "file":
                    await m.message.reply_to_message.reply_chat_action("upload_document")
                    await bot.send_document(
                        chat_id=m.message.chat.id,
                        document=download_directory,
                        thumb=thumb_nail,
                        caption=description,
                        parse_mode="HTML",
                        reply_to_message_id=m.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Presets.UPLOAD_START,
                            m.message,
                            start_time,
                            bot,
                            id
                        )
                    )
                elif tg_send_type == "vm":
                    await m.message.reply_to_message.reply_chat_action("upload_video_note")
                    await bot.send_video_note(
                        chat_id=m.message.chat.id,
                        video_note=download_directory,
                        thumb=thumb_nail,
                        duration=duration,
                        reply_to_message_id=m.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Presets.UPLOAD_START,
                            m.message,
                            start_time,
                            bot,
                            id
                        )
                    )
                elif tg_send_type == "video":
                    await m.message.reply_to_message.reply_chat_action("upload_video")
                    await bot.send_video(
                        chat_id=m.message.chat.id,
                        video=download_directory,
                        caption=description,
                        parse_mode="HTML",
                        supports_streaming=True,
                        duration=duration,
                        thumb=thumb_nail,
                        reply_to_message_id=m.message.reply_to_message.message_id,
                        progress=progress_for_pyrogram,
                        progress_args=(
                            Presets.UPLOAD_START,
                            m.message,
                            start_time,
                            bot,
                            id
                        )
                    )
                else:
                    pass
            try:
                shutil.rmtree(tmp_directory_for_each_user)   
            except Exception:
                pass
            await bot.delete_messages(
                m.message.chat.id,
                m.message.message_id
            )
