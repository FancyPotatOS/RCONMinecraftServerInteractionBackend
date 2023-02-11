######### https://www.geeksforgeeks.org/python-import-from-parent-directory/ ##########
import path
import sys
 
# directory reach
directory = path.Path(__file__).abspath()
 
# setting path
sys.path.append(directory.parent.parent)
###################

from mcrcon import *
import time

colors = {	
    "white": "white",
    "orange" : "#FFA500",
    "magenta" : "#FF00FF",
    "light_blue" : "#ADD8E6",
	"yellow": "yellow",
	"lime": "#32CD32",
	"pink": "#ffc0cb",
	"gray": "gray",
	"light_gray": "#D3D3D3",
	"cyan": "#00FFFF",
	"purple": "light_purple",
	"blue": "blue",
	"brown": "#964B00",
	"green": "green",
	"red": "red",
	"black": "black"
}

client = MinecraftRCon('192.168.2.28', 25574, '12345')

storage = client.get_storage("hoppercounter:main")

collected = {}
while True:

    client.run("function hoppercounter:count_all")

    stored = storage.get()

    for hopper in stored["hoppers"]:
        for item in hopper["Items"]:
            if not item["id"] in collected:
                collected[item["id"]] = { 
                    "count": 0, 
                    "start_time": time.time()-0.125 
                }
            collected[item["id"]]["count"] = collected[item["id"]]["count"] + item["Count"]

    if len(collected) > 0:

        formatted_items = []
        for item in collected:
            has_color = False
            found_color = None
            for color in colors:
                if color in item:
                    has_color = True
                    found_color = color
            
            id_name = item.replace("minecraft:", "").replace("_", " ").title()
            amount = str(int(collected[item]["count"]))
            amount_per_sec = (str(int(collected[item]["count"] / (time.time() - collected[item]["start_time"]))))

            if found_color is not None:
                formatted_items.append('{"text":"' + id_name + '","color":"' + colors[found_color] + '"},{"text":": ' + amount + ' (' + amount_per_sec + '/sec); ","color":"white"}')
            else:
                formatted_items.append('{"text":"' + id_name + '","color":"white"},{"text":": ' + amount + ' (' + amount_per_sec + '/sec); ","color":"white"}')

        formatted_items[-1] = formatted_items[-1].replace("; ", "")
        tellraw_coll = ""

        actionbar_command = 'title @a actionbar [' + ','.join(formatted_items) + ']'
        actionbar_show_command = 'title @a title {"text":""}'

        storage.merge("{hoppers:[]}")

        client.run(actionbar_command)
        client.run(actionbar_show_command)


    time.sleep(1)

client.conn.close()
