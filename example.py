#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:   Darth-Revan
# Name:     imgur-dl.py
# Version:  1.0
# Date:     August 16th 2016
# License:  MIT

"""
This file provides an example in using *imgur-dl* in other python programs.
"""

import imgur_dl

downloader = imgur_dl.ImgurDownloader("https://imgur.com/a/Y8D4O", use_name=True)
print(downloader.get_title())
print(downloader.get_album_id())
print(downloader.get_uploader())
print(downloader.get_image_count())
downloader.download_images()
