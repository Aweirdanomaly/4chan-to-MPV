import requests
import re
from bs4 import BeautifulSoup
import sys
import os
os.environ["PATH"] = os.path.abspath('') + os.pathsep + os.environ["PATH"]
import mpv
import json
from colorama import Fore, Style
import random 
import argparse
import html
import cowsay

rabbit = r'''
\
   (\(\
  ( -.-)
  o_(")(")
'''

def getThreads():
    ans = requests.get("https://boards.4chan.org/wsg/catalog")
    soup = BeautifulSoup(ans.text, 'html.parser')
    scripts = soup.find_all("script")
    script = [s for s in scripts if len(s.text)>400][0].text
    catalog_pattern = r'var\s+catalog\s*=\s*({.*?});'
    dictJS = re.search(catalog_pattern, script, re.DOTALL).group(1)
    d= json.loads(dictJS)
    return ([{"filename" :html.unescape(d['threads'][num]['sub'] + ' ' + d['threads'][num]['teaser']), "id":idx} for idx, num in enumerate(d['threads']) if num != '957536'], [num for num in d['threads'] if num != '957536'])
    # return [thread for thread in d["threads"] if "ygyl" in d["threads"][thread]["sub"].lower()]
    
def getVids(d):
    ans = requests.get(f"https://boards.4chan.org/wsg/thread/{d}")
    soup = BeautifulSoup(ans.text, 'html.parser')
    links = soup.find_all("a", class_ ="fileThumb")
    return [f"https:{link['href']}" for link in links]


def prettyPrint(vids, current=-1, page=-1):


    columns, lines = os.get_terminal_size()
    lines-=3
    ceiling = lambda a,b : -(a//-b) 
    pages = ceiling(len(vids), lines)
    if page>pages or current>len(vids):
        print("Invalid page or video selection")
        return
    current_page = int(ceiling(current+.01, lines)) if current > 0 else page if page > 0 else 1
    # print(current, columns, lines, pages, current_page, ceiling(current, lines))
    # print("here: " ,current_page)
    strings = [f"{vid['id']}{' '*(4-len(str(vid['id'])))}{vid['filename']} "[:columns] if vid['id'] != current+1 else f"> {vid['id']}{' '*(4-len(str(vid['id'])))}{vid['filename']}" for vid in vids[(current_page-1)*lines:(current_page*lines)] ]
    for line in strings:
        print(Fore.BLUE + line if line[0]!='>' else Fore.RED + line)
    print(Style.RESET_ALL)


def playVids(vids, **kwargs):
    
    player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, terminal=True, input_terminal=True, osc=True, really_quiet=True, loglevel='terminal-default',  **kwargs) 


    for vid in vids:
        player.playlist_append(vid)
    
    @player.on_key_press('ESC')
    def my_esc_binding():
        print("ESC pressed")
        player.quit(0)
        
    @player.on_key_press('Shift+S')
    def shuffle():
        print(player.playlist_pos)
        player.playlist_shuffle()
        print(player.playlist)
        
    # @player.on_key_press('Ctrl+S')
    # def unshuffle():
    #     player.playlist_unshuffle()
    #     print(player.playlist)

    player.on_key_press('ENTER')(lambda: player.playlist_next(mode='force') if player.playlist_pos >= 0 else None)
    player.on_key_press('Shift+ENTER')(lambda: player.playlist_prev(mode='force') if player.playlist_pos <= len(player.playlist) else None)
    
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
        # player.wait_for_playback() Will use this if allow to queue any video order
        print("done")
    except mpv.ShutdownError:
        pass
    player.terminate()     
    # player.quit(0)


def find(query):
    #look for threads with query in them
    pass


def parseChoice(choiceList, page):
    
    columns, lines = os.get_terminal_size()
    lines-=3
    ceiling = lambda a,b : -(a//-b) 
    max_pages = ceiling(len(choiceList), lines)


    while True:
        # prettyPrint(choiceList, page=page)
        choice = input("Enter number choice, 'n' or 'p' to change pages, or 'q' to quit:\n > ")

        match (choice):
            case ('q'):
                cowsay.draw('Goodbye...', rabbit)
                sys.exit()
            case ('n') :
                if page+1 <= max_pages:
                    page+=1
                    prettyPrint(choiceList, page=page)
                else:
                    # prettyPrint(choiceList, page=page)
                    print(Fore.RED + "There are no further pages")
                    print(Style.RESET_ALL)
            case ('p'):
                if page-1 >= 1:
                    page-=1
                    prettyPrint(choiceList, page=page)
                else:
                    # prettyPrint(choiceList, page=page)
                    print(Fore.RED + "There are no more previous pages")
                    print(Style.RESET_ALL)
            # case 'f':
            #     query = input("Enter string to search for:\n")
            #     find(query)
            case num:
                match (num.isdigit()):
                    case True:
                        t = int(num)
                        if t >= 0 and t < len(choiceList):
                            return int(num)-1
                    case False:
                        # prettyPrint(choiceList, page=page)
                        print(Fore.RED + "Unknown command")
                        print(Style.RESET_ALL)
        

def main():
    parser = argparse.ArgumentParser(prog='42M', description="Make a playlist out of a 4chan thread")
    parser.add_argument('--no-video', dest='video', action='store_false', default='auto')
    parser.add_argument('-query', required=False, type=str, help='type of thread to look for')
    parser.add_argument('-a', dest='audio', type=str, help='Plays audio only, no video')

    


    args = parser.parse_args()


    # print(args.query)

    threads, links = getThreads()
    #choose desired thread
    while True: 
        prettyPrint(threads)
        chosenThread = parseChoice(threads, 1)


        #get thread vids

        prettyPrint(threads, chosenThread)
        vids = getVids(links[chosenThread])
        random.shuffle(vids)

        #choose vids
        playVids(vids, video=args.video)


if __name__ == "__main__":
    main()