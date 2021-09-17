# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name     : inline-tube-mate [ Telegram ]
# Repo     : https://github.com/m4mallu/inine-tube-mate
# Author   : Renjith Mangal [ https://t.me/space4renjith ]
# Credits  : https://github.com/SpEcHiDe/AnyDLBot

import math
import time
from presets import Presets
from library.buttons import reply_markup_cancel

cancel_process = {}

async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start,
    bot,
    id
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}\n𝐒𝐭𝐚𝐭𝐮𝐬   : {2}%\n".format(
            ''.join([Presets.FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 7.6923))]),
            ''.join([Presets.UN_FINISHED_PROGRESS_STR for i in range(13 - math.floor(percentage / 7.6923))]),
            round(percentage, 2))

        tmp = progress + "𝐏𝐫𝐨𝐜𝐞𝐬𝐬 : {0}  𝐎𝐟  {1}\n𝐒𝐩𝐞𝐞𝐝    : {2}/s\n𝐖𝐚𝐢𝐭𝐢𝐧𝐠 : {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                "{}\n {}".format(
                    ud_type,
                    tmp,
                ),
                reply_markup=reply_markup_cancel
            )
        except Exception:
            pass
    if id not in cancel_process:
        bot.stop_transmission()

def humanbytes(size):
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
