# Doom Chan

This CLI lets you browse 4chan from the terminal and make a playlist out of any thread, streamlining the experience and making it more doomscroll-able. 

![DemoVideo](./assets/demo.gif)

Although this was originally made to turn video-heavy threads from [/wsg/](https://4chan.org/wsg/catalog) into playlists (YGYL threads mostly), all threads on all boards on 4chan are now supported, including those with just images present.

The order of videos is also always shuffled to keep it fresh.

## Usage

Run `dc` to launch the cli

- `b` switches between boards and displays their threads
- `f` searches for a specific string in thread titles
- numbers are used to select boards and threads
- `Enter` and `Shift+Enter` can be used to go to the next and previous videos in the playlist and `Esc` quits the playlist
- `q` quits the CLI

All the mpv key bindings can also be used for this cli, so `[` and `]` can be used to change the speed of the video and the arrow keys can be used to seek within the video. If you're unfamiliar with mpv, here's a full list of all the [keyboard controls](https://mpv.io/manual/master/#keyboard-control).



## Requirements

- [Python](https://www.python.org/downloads/) (version 3.10 or above)
- [MPV](https://mpv.io/installation/)


## Installation

Once you have the requirements set up, just run `pip install doom_chan` and everything will be installed.

-----------------------------------------------------
If you like installing things the _hard_ way, you can also just download and use `./doom_chan/doom_chan.py` since all the code is entirely contained there. 

However, Windows users (and only Windows users) will also need to download and install [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/). After the download, extract the folder, then place `libmpv-2.dll` in the same folder as `doom_chan.py`.

You don't need to worry about any of this if you just install this project with `pip` though.

## Uninstallation

Run `pip uninstall doom_chan`

## Contributions

Pull requests are always welcome, but please do open an issue first if you plan on implementing major changes.

## Inspiration

This library was inspired by projects like [yewtube](https://github.com/mps-youtube/yewtube) and [ani-cli](https://github.com/pystardust/ani-cli) which scrape the internet and let you surf🏄 platforms from a CLI.

This project would also not have been possible without [python-mpv](https://github.com/jaseg/python-mpv). If it weren't for this library, I would not have been able to connect to mpv with Python.
