# imgur-dl
A simple command line tool for downloading albums from imgur.com

## Requirements

*imgur-dl* is completely written it Python 3. I developed it using the 3.5 release of Python. I am quite sure, that the
script will run on any 3.x version, but I strongly recommend to always use the latest, of course.

*imgur-dl* requires some Python modules to be able to do its work. Most of them are part of any standard Python installation.
There is only one module you may need to install by yourself: the one and only *BeautifulSoup4*.

Simply install it with *pip* with:

```
pip3 install beautifulsoup4
```

## Usage

I tried to keep the usage of *imgur-dl* as easy as possible by providing a reasonable amount of command line options.
In order to execute the program, install Python (>= 3.x), the required module(s) and execute the script with a simple
`python3 imgur_dl.py`.

You can inspect the usage information of the script by invoking `python3 imgur_dl.py -h` or `python3 imgur_dl.py --help`:

```
usage: imgur_dl.py [-h] -u URL [-d DEST] [-n] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The album's url you want to download.
  -d DEST, --destination DEST
                        Path to the folder in which you want to store the
                        downloaded images. If not given, the program creates a
                        new folder in the current directory out of the album's
                        id.
  -n, --name            By setting this flag the name of the specified album
                        will be used for the output path instead of its id
                        (-d/--destination overwrites this value).
  -v, --version         show program's version number and exit
```

## Using *imgur-dl* in other Python programs

Of course, you can also import *imgur-dl* in your own Python code and use its few features. Simply add a new line
(usually somewhere at the top of the source file) reading:

```
import imgur_dl
```

Afterwards you can create a new instance of the base downloader class and download the images:

```
imgdl = imgur_dl.ImgurDownloader("<ALBUM URL>", "<DESTINATION PATH>")
imgdl.download_images()
```

There are a few methods in this class you may (or may not) find helpful when using the class. These include:

 - get_album_id() -- Returns the album's id number
 - get_title() -- Returns the album's title
 - get_uploader() -- Returns the uploader's name
 - get_image_count() -- Returns the number of images in the album
 - download_images() -- Downloads the images from the album and saves them on disk

## Disclaimer

Although imgur.com strongly emphasizes that uploaders of images and albums have to make sure to not to violate copyright
laws by uploading files, you can't always be sure, of course.

**I am, in no way responsible for any violation of copyright laws that may or may not occur by downloading images with this tool.**

## License

This script is provided under the terms of the MIT License. For the full text of the license, see the file **LICENSE**.
