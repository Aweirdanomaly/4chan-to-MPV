import requests
import re
from bs4 import BeautifulSoup
import os
os.environ["PATH"] = os.path.abspath('') + os.pathsep + os.environ["PATH"]
import mpv
import json
from colorama import Fore, Style
import random 
import argparse

def getThreads():
    ans = requests.get("https://boards.4chan.org/wsg/catalog")
    soup = BeautifulSoup(ans.text, 'html.parser')
    scripts = soup.find_all("script")
    script = [s for s in scripts if len(s.text)>400][0].text
    catalog_pattern = r'var\s+catalog\s*=\s*({.*?});'
    dictJS = re.search(catalog_pattern, script, re.DOTALL).group(1)
    d= json.loads(dictJS)
    return [thread for thread in d["threads"] if "ygyl" in d["threads"][thread]["sub"].lower()]
    
def getVids(d):
    ans = requests.get(f"https://boards.4chan.org/wsg/thread/{d[0]}")
    soup = BeautifulSoup(ans.text, 'html.parser')
    links = soup.find_all("a", class_ ="fileThumb")
    return [f"https:{link["href"]}" for link in links]


def prettyPrint(vids, current=-1):


    columns, lines = os.get_terminal_size()
    lines-=3
    ceiling = lambda a,b : -(a//-b) 
    pages = ceiling(len(vids), lines)
    current_page = int(ceiling(current+.01, lines)) if current > 0 else 1
    print(current, columns, lines, pages, current_page, ceiling(current, lines))
    print("here: " ,current_page)
    strings = [f"{vid['id']}{" "*(4-len(str(vid['id'])))}{vid['filename']} " if vid['id'] != current+1 else f"> {vid['id']}{" "*(4-len(str(vid['id'])))}{vid['filename']}" for vid in vids[(current_page-1)*lines:(current_page*lines)] ]
    for line in strings:
        print(Fore.BLUE + line if line[0]!='>' else Fore.RED + line)
    print(Style.RESET_ALL)


def playVids(vids, **kwargs):
    
    player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, terminal=True, input_terminal=True, osc=True, really_quiet=True, **kwargs) 


    for vid in vids:
        player.playlist_append(vid)
    
    @player.on_key_press('ESC')
    def my_esc_binding():
        print("ESC pressed")
        player.quit(0)
        
    player.on_key_press('ENTER')(lambda: player.playlist_next(mode='force'))
    player.on_key_press('Shift+ENTER')(lambda: player.playlist_prev(mode='force'))

    # @player.property_observer('playlist')
    # def my_handler(property_name, files):
    #     # filenames = [file['filename'] for file in files]
    #     current_index = next((idx for idx, el in enumerate(files) if el.get('current')), -1)
    #     prettyPrint(files, current_index)
    
    @player.property_observer('playlist-pos')
    def my_handler(property_name, pos):
        prettyPrint(player.playlist, pos)
        
    @player.event_callback('shutdown')
    def close(event):
        if player._core_shutdown:
            player.quit(0)

    player.playlist_play_index(0)
    
    try:
        player.wait_for_property('idle-active')
    except mpv.ShutdownError:
        pass
    player.terminate()     


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-video', dest='video', action='store_false', default='auto')
    args = parser.parse_args()


    vids = (getVids(getThreads()))
    random.shuffle(vids)
    playVids(vids, video=args.video)


if __name__ == "__main__":
    main()