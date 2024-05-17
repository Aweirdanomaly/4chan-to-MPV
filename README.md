# 4Chan to MPV (42M for short)

This library lets you make a playlist out of any thread on 4chan's [/wsg/ board](https://4chan.org/wsg/catalog)

Demo Vid goes here (just imagine there is one here for now)

## Requirements

- [Python](https://www.python.org/downloads/) (version 3.9 or above)
- [MPV](https://mpv.io/installation/)

##### Windows Only:

- [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/) (download and extract the folder, then place `libmpv-2.dll` wherever you download this library)

## Installation

1- Download 42M.py and requirements.txt
2- Run `pip install -r requirements.txt`

## Usage

Go into the directory where 42M.py is located and run `python 42M.py`

## Uninstallation

This project is entirely contained in 42M.py, so just delete it lmao

## TODO

This project (although functional) is still in early development and is meant to be expanded upon. Here are some of the features that I'm still implementing:

- Allow for scraping other threads that aren't YGYL
- Make a main menu that allows the user to select other threads
- Actually make a Demo vid for the readme
- Scrape for post content
- Add shuffle button option instead of leaving it on by default
- Parse a variety of commands like audio only
- Get lib approved on PyPl for easier installing

## Inspiration

This library was inspired by projects like [yewtube](https://github.com/mps-youtube/yewtube) and [ani-cli](https://github.com/pystardust/ani-cli) which scrape the internet and let you surf🏄 platforms from a CLI.

This project would also not have been possible without [python-mpv](https://github.com/jaseg/python-mpv). If it weren't for this library, I would not be able to write this in Python.
