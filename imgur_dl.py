#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:   Darth-Revan
# Name:     imgur-dl.py
# Version:  1.0
# Date:     August 16th 2016
# License:  MIT

from argparse import ArgumentParser
import sys
import re
import urllib.request as req
from os.path import exists, realpath, join, splitext
from os import makedirs, remove
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[Error] Failed to import BeautifulSoup4. Sorry, not able to run without it!")
    sys.exit(1)


class ImgurException(Exception):
    """
    Just a very simple Exception to raise when certain errors occur.
    """

    def __init__(self, msg):
        super(ImgurException, self).__init__(msg)


class ImgurDownloader(object):
    """
    Base class for downloading albums from imgur.com. Provides some basic functions for extracting information from the
    album.
    """

    def __init__(self, url, dest_path=None, use_name=False):
        """
        Constructor for the class **ImgurDownloader**.

        :param url: The album's url
        :type url: str
        :param dest_path: Path to a folder in which the images will be stored
        :type dest_path: str
        :param use_name: Use the album's name instead of its id to generate a folder name if dest_path is not provided
        :type use_name: bool
        """
        self.url = str(url)
        self.use_name = bool(use_name)
        self.dest = dest_path
        self.album_id = self.__validate_url__()

        try:
            self.response = req.urlopen(url="http://imgur.com/a/{}/layout/blog".format(self.album_id))
            self.resp_code = self.response.getcode()
        except Exception as e:
            self.response = None
            self.resp_code = e.code

        if self.response is None or self.resp_code != 200:
            raise ImgurException("Error while requesting album from imgur.com: Got " +
                                 "response code {}".format(str(self.resp_code)))

        content = self.response.read().decode('utf-8')
        self.soup = BeautifulSoup(content, "html.parser")
        self.title = str(self.soup.find('h1', class_="post-title").string)
        images = self.soup.find('div', class_="post-images").findAll('a', class_="zoom")
        self.image_list = []
        for image in images:
            self.image_list.append(image.get('href'))

    def __validate_url__(self):
        """
        Validates the attribute **url** of the object. If validation fails, an **ImgurException** will be raised.
        Otherwise the function returns the album's id as a string.
        """
        match = re.match(r"(https?)\:\/\/(www\.)?(?:m\.)?imgur\.com/(a|gallery)/([a-zA-Z0-9]+)(#[0-9]+)?", self.url)
        if not match:
            raise ImgurException("The url \"{}\" is not valid!".format(str(self.url)))
        return match.group(4)

    def get_album_id(self):
        """
        Returns the album's id as a string.

        :return: The album's id
        :rtype: str
        """
        return str(self.album_id)

    def get_title(self):
        """
        Returns the album's name as a string.

        :return: The album's name
        :rtype: str
        """
        return str(self.title)

    def get_uploader(self):
        """
        Returns the album's uploader as a string.

        :return: The album's uploader
        :rtype: str
        """
        uploader = self.soup.find('a', class_="post-account").string
        return str(uploader).strip()

    def get_image_count(self):
        """
        Returns the number of images in the album.

        :return: The number of images
        :rtype: int
        """
        return len(self.image_list)

    def download_images(self):
        """
        Downloads all images from the album and saves them on disk.

        :return: None
        """
        if self.dest is None:
            folder = self.get_title() if self.use_name else self.album_id
        else:
            folder = self.dest
        folder = realpath(folder)
        if not exists(folder):
            makedirs(folder)
        count = 1
        successful = 0
        for image in self.image_list:
            outpath = join(folder, "{}{}".format(count, splitext(image)[1]))
            if exists(outpath):
                print("[WARNING] The image file \"{}\" does already exist. Skipping...".format(outpath))
            else:
                try:
                    print("Downloading image from {} ({} of {})".format(image, count, len(self.image_list)))
                    req.urlretrieve("https:" + image, outpath)
                    successful += 1
                except:
                    print("[ERROR] Failed to download image from URL {}".format(image))
                    remove(outpath)
            count += 1
        print("\nSuccessfully downloaded {} images to {}".format(successful, folder))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", required=True, action="store", type=str, dest="url",
                        help="The album's url you want to download.")
    parser.add_argument("-d", "--destination", required=False, action="store", type=str, dest="dest",
                        help="Path to the folder in which you want to store the downloaded images. If not given, the " +
                        "program creates a new folder in the current directory out of the album's id.")
    parser.add_argument("-n", "--name", required=False, action="store_true", dest="name", help="By setting this flag " +
                        "the name of the specified album will be used for the output path instead of its id " +
                        "(-d/--destination overwrites this value).")
    parser.add_argument("-v", "--version", action="version", version="imgur-dl version 1.0")
    parsed = parser.parse_args()
    try:
        imgdl = ImgurDownloader(parsed.url, parsed.dest, parsed.name)
        imgdl.download_images()
    except ImgurException as e:
        print("[ERROR] {}".format(str(e)))
