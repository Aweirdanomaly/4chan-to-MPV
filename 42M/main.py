import requests
import re
from bs4 import BeautifulSoup
import sys
import platform
import os
#Add env variable to path if on Windows
if platform.system() == 'Windows':
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

### Hardcoded boards since scraping their names requires captcha. Update list if any new ones drop
boards=[{'filename': '/a/ Anime & Manga', 'id': 1},
 {'filename': '/c/ Anime/Cute', 'id': 2},
 {'filename': '/w/ Anime/Wallpapers', 'id': 3},
 {'filename': '/m/ Mecha', 'id': 4},
 {'filename': '/cgl/ Cosplay & EGL', 'id': 5},
 {'filename': '/cm/ Cute/Male', 'id': 6},
 {'filename': '/f/ Flash', 'id': 7},
 {'filename': '/n/ Transportation', 'id': 8},
 {'filename': '/jp/ Otaku Culture', 'id': 9},
 {'filename': '/vt/ Virtual YouTubers', 'id': 10},
 {'filename': '/v/ Video Games', 'id': 11},
 {'filename': '/vg/ Video Game Generals', 'id': 12},
 {'filename': '/vm/ Video Games/Multiplayer', 'id': 13},
 {'filename': '/vmg/ Video Games/Mobile', 'id': 14},
 {'filename': '/vp/ Pokémon', 'id': 15},
 {'filename': '/vr/ Retro Games', 'id': 16},
 {'filename': '/vrpg/ Video Games/RPG', 'id': 17},
 {'filename': '/vst/ Video Games/Strategy', 'id': 18},
 {'filename': '/co/ Comics & Cartoons', 'id': 19},
 {'filename': '/g/ Technology', 'id': 20},
 {'filename': '/tv/ Television & Film', 'id': 21},
 {'filename': '/k/ Weapons', 'id': 22},
 {'filename': '/o/ Auto', 'id': 23},
 {'filename': '/an/ Animals & Nature', 'id': 24},
 {'filename': '/tg/ Traditional Games', 'id': 25},
 {'filename': '/sp/ Sports', 'id': 26},
 {'filename': '/xs/ Extreme Sports', 'id': 27},
 {'filename': '/pw/ Professional Wrestling', 'id': 28},
 {'filename': '/sci/ Science & Math', 'id': 29},
 {'filename': '/his/ History & Humanities', 'id': 30},
 {'filename': '/int/ International', 'id': 31},
 {'filename': '/out/ Outdoors', 'id': 32},
 {'filename': '/toy/ Toys', 'id': 33},
 {'filename': '/i/ Oekaki', 'id': 34},
 {'filename': '/po/ Papercraft & Origami', 'id': 35},
 {'filename': '/p/ Photography', 'id': 36},
 {'filename': '/ck/ Food & Cooking', 'id': 37},
 {'filename': '/ic/ Artwork/Critique', 'id': 38},
 {'filename': '/wg/ Wallpapers/General', 'id': 39},
 {'filename': '/lit/ Literature', 'id': 40},
 {'filename': '/mu/ Music', 'id': 41},
 {'filename': '/fa/ Fashion', 'id': 42},
 {'filename': '/3/ 3DCG', 'id': 43},
 {'filename': '/gd/ Graphic Design', 'id': 44},
 {'filename': '/diy/ Do-It-Yourself', 'id': 45},
 {'filename': '/wsg/ Worksafe GIF', 'id': 46},
 {'filename': '/qst/ Quests', 'id': 47},
 {'filename': '/biz/ Business & Finance', 'id': 48},
 {'filename': '/trv/ Travel', 'id': 49},
 {'filename': '/fit/ Fitness', 'id': 50},
 {'filename': '/x/ Paranormal', 'id': 51},
 {'filename': '/adv/ Advice', 'id': 52},
 {'filename': '/lgbt/ LGBT', 'id': 53},
 {'filename': '/mlp/ Pony', 'id': 54},
 {'filename': '/news/ Current News', 'id': 55},
 {'filename': '/wsr/ Worksafe Requests', 'id': 56},
 {'filename': '/vip/ Very Important Posts', 'id': 57},
 {'filename': '/b/ Random', 'id': 58},
 {'filename': '/r9k/ ROBOT9001', 'id': 59},
 {'filename': '/pol/ Politically Incorrect', 'id': 60},
 {'filename': '/bant/ International/Random', 'id': 61},
 {'filename': '/soc/ Cams & Meetups', 'id': 62},
 {'filename': '/s4s/ Shit 4chan Says', 'id': 63},
 {'filename': '/s/ Sexy Beautiful Women', 'id': 64},
 {'filename': '/hc/ Hardcore', 'id': 65},
 {'filename': '/hm/ Handsome Men', 'id': 66},
 {'filename': '/h/ Hentai', 'id': 67},
 {'filename': '/e/ Ecchi', 'id': 68},
 {'filename': '/u/ Yuri', 'id': 69},
 {'filename': '/d/ Hentai/Alternative', 'id': 70},
 {'filename': '/y/ Yaoi', 'id': 71},
 {'filename': '/t/ Torrents', 'id': 72},
 {'filename': '/hr/ High Resolution', 'id': 73},
 {'filename': '/gif/ Adult GIF', 'id': 74},
 {'filename': '/aco/ Adult Cartoons', 'id': 75},
 {'filename': '/r/ Adult Requests', 'id': 76}]

def getThreads(board='wsg'):
    ans = requests.get(f"https://boards.4chan.org/{board}/catalog")
    soup = BeautifulSoup(ans.text, 'html.parser')
    scripts = soup.find_all("script")
    script = [s for s in scripts if len(s.text)>400][0].text
    catalog_pattern = r'var\s+catalog\s*=\s*({.*?});'
    dictJS = re.search(catalog_pattern, script, re.DOTALL).group(1)
    d= json.loads(dictJS)
    #filter stickies here
    return ([{"filename" :html.unescape(d['threads'][num]['sub'] + f"{'' if d['threads'][num]['sub']=='' else ' '}" + d['threads'][num]['teaser']).replace("\n", ""), "id":idx+1} for idx, num in enumerate(d['threads']) ], [num for num in d['threads']])
    # return [thread for thread in d["threads"] if "ygyl" in d["threads"][thread]["sub"].lower()]
    
def getVids(state):
    ans = requests.get(f"https://boards.4chan.org/{state['board']}/thread/{state['links'][state['threadIdx']]}")
    soup = BeautifulSoup(ans.text, 'html.parser')
    links = soup.find_all("a", class_ ="fileThumb")
    return [f"https:{link['href']}" for link in links]




def prettyPrint(vids, current=-1, page=-1):
    columns, lines = os.get_terminal_size()
    lines-=4
    ceiling = lambda a,b : -(a//-b) 
    pages = ceiling(len(vids), lines)
    if page>pages or current>len(vids):
        print(Fore.RED + "Invalid page or video selection" + Style.RESET_ALL)
        return
    current_page = int(ceiling(current+.01, lines)) if current > 0 else page if page > 0 else 1
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
        
    # @player.on_key_press('Shift+S')
    # def shuffle():
    #     print(player.playlist_pos)
    #     player.playlist_shuffle()
    #     print(player.playlist)
        
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


def getTerminalSize(state):
    columns, lines = os.get_terminal_size()
    state['terminal']['columns']=columns
    state['terminal']['lines']=lines-4
    ceiling = lambda a,b : -(a//-b) 
    state['terminal']['max_pages']= ceiling(len(state['choiceList']), lines)
    return state

def getListInfo(state):
    state["choiceList"], state["links"] = getThreads(state['board'])
    return state


def parseChoice(state):
    
    state = getTerminalSize(state)
    prettyPrint(state['choiceList'], page=state['terminal']['page'])

    while True:
        print(Fore.GREEN + f"Page {state['terminal']['page']} out of {state['terminal']['max_pages']}" + Style.RESET_ALL)
        choice = input(f"Enter number choice, 'n' or 'p' to change pages, 'b' to change boards, or 'q' to quit:\n > ")
        state = getTerminalSize(state)
        match (choice):
            case ('q'):
                cowsay.draw('Goodbye...', rabbit)
                sys.exit()
            case ('n') :
                if state['terminal']['page']+1 <= state['terminal']['max_pages']:
                    state['terminal']['page']+=1
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])
                else:
                    state['terminal']['page'] = state['terminal']['max_pages']
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])
                    print(Fore.RED + "There are no further pages")
                    print(Style.RESET_ALL)
            case ('p'):
                if state['terminal']['page']-1 >= state['terminal']['max_pages']:
                    state['terminal']['page'] = state['terminal']['max_pages']
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])

                elif state['terminal']['page']-1 >= 1:
                    state['terminal']['page']-=1
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])
                else:
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])
                    print(Fore.RED + "There are no more previous pages")
                    print(Style.RESET_ALL)
            case 'f':
                query = input("Enter string to search for:\n")
                results = ([entry for entry in state['choiceList'] if query.lower() in entry['filename'].lower()])
                print(Fore.RED + "No Results Found" + Style.RESET_ALL) if results==[] else prettyPrint(results)
            case 'b':
                if state["boardSelection"]:
                    state["boardSelection"]=False
                    state['choiceList']=boards
                    chosenBoard = parseChoice(state)
                    state["boardSelection"]=True
                    prettyPrint(boards, page=state['terminal']['page'], current=chosenBoard)
                    state['board']= state['choiceList'][chosenBoard]['filename'].split(' ')[0][1:-1]
                    state=getListInfo(state)
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])
                else:
                    prettyPrint(state['choiceList'], page=state['terminal']['page'])
                    print(Fore.RED + "You are already selecting a board")
                    print(Style.RESET_ALL)
            case num:
                match (num.isdigit()):
                    case True:
                        t = int(num)
                        if t >= 0 and t < len(state['choiceList']):
                            return int(num)-1
                    case False:
                        prettyPrint(state['choiceList'], page=state['terminal']['page'])
                        print(Fore.RED + "Unknown command" + Style.RESET_ALL)
        

def main():
    parser = argparse.ArgumentParser(prog='42M', description="Make a playlist out of a 4chan thread")
    parser.add_argument('--no-video', dest='video', action='store_false', default='auto')
    parser.add_argument('-query', required=False, type=str, help='type of thread to look for')
    parser.add_argument('-a', dest='audio', type=str, help='Plays audio only, no video')

    


    args = parser.parse_args()


    # print(args.query)

    # print("passed")



    state = {
        'terminal': 
            {
            'columns': 0,
            'lines': 0,
            'max_pages': 0,
            'page': 1
            },
        'board': 'wsg',
        'boardSelection': True,
        'choiceList': [],
        'links': [],
        'threadIdx': 1
    }
    #scrape info
    state=getListInfo(state)

    while True: 
        #choose params
        state['threadIdx'] = parseChoice(state)

        #get thread vids
        prettyPrint(state['choiceList'], state['threadIdx'])
        vids = getVids(state)
        random.shuffle(vids)

        #mpv vids
        playVids(vids, video=args.video)

if __name__ == "__main__":
    main()