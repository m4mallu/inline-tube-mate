""" !/usr/bin/env python3
    -*- coding: utf-8 -*-
    Name     : inline-tube-mate [ Telegram ]
    Repo     : https://github.com/m4mallu/inine-tube-mate
    Author   : Renjith Mangal [ https://t.me/space4renjith ]
    Credits  : https://github.com/SpEcHiDe/AnyDLBot """

import os
import wget
from youtubesearchpython import *

async def youtube_search(query):
    sear = VideosSearch(query)
    result = sear.result()['result']
    return result

async def yt_link_search(url):
    videoInfo = Video.getInfo(url, mode=ResultMode.dict)
    return videoInfo

async def yt_thumb_dl(thumb_url, m):
    yt_thumb_image_path = os.getcwd() + "/" + "YThumb" + "/" + str(m.from_user.id) + ".jpg"
    yt_thumb_dir = os.getcwd() + "/" + "YThumb" + "/"
    if not os.path.isdir(yt_thumb_dir):
        os.makedirs(yt_thumb_dir)
    else:
        try:
            for f in os.listdir(yt_thumb_dir):
                os.remove(os.path.join(yt_thumb_dir, f))
        except Exception:
            pass
    thumb = wget.download(thumb_url, yt_thumb_image_path, bar=None)
    return thumb
