
from rcon.source import Client

import re
import relaxedjson

class MinecraftStorage:
    def __init__(self, mrcon, namespace):
        self.mrcon = mrcon
        if not re.match(r"^([_\-.a-zA-Z0-9]+:)?[_\-.a-zA-Z0-9]+(\/[_\-.a-zA-Z0-9]+)*$", namespace):
            raise ValueError("Invalid namespace")
        self.namespace = namespace
    
    def get(self, target=""):
        cmd = "data get storage " + self.namespace
        if not target == "":
            cmd += " " + target
        response = self.mrcon.run(cmd)

        if re.match(r"^Found no elements matching.*$", response) is not None:
            raise ValueError("Invalid target")

        # Remove trailing number type designation /leading array number type designation (10b or [I; 0, 1, 2])
        response = re.sub("((?<=[0-9])[bBdDlLsSfFiI](?=[^0-9]))|((?<=\[)[bBdDlLsSfFiI];)", "", response)

        cleaned = ' '.join(response.split(" ")[6:])

        value = relaxedjson.parse(cleaned)

        return value
    
    def merge(self, value):
        cmd = "data merge storage " + self.namespace + " " + value
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown or incomplete command.*$", response) is not None:
            raise ValueError("No value given to merge")
        elif re.match(r"^Expected.*$", response) is not None:
            raise ValueError("Invalid value")
    
    def remove(self, path):
        cmd = "data remove storage " + self.namespace + " " + path
        response = self.mrcon.run(cmd)

        if re.match(r"^Invalid NBT.*$", response) is not None:
            raise ValueError("Invalid path")
        if re.match(r"^Unknown or incomplete command.*$", response) is not None:
            raise ValueError("No path given to merge")
    
    def modifyfrom(self, path, method, source, parameters):
        methods = ["append", "insert", "merge", "prepend", "set"]
        sources = ["block", "entity", "storage"]

        if not method in methods:
            raise ValueError("Invalid method")
        if not source in sources:
            raise ValueError("Invalid source")
        
        cmd = "data modify storage " + self.namespace + " " + path + " " + method + " from " + source + " " + parameters
        response = self.mrcon.run(cmd)

        if re.match(r"^Invalid NBT.*$", response) is not None:
            raise ValueError("Invalid path")
        if re.match(r"^Unknown or incomplete command.*$", response) is not None:
            raise ValueError("Incomplete command")
        if re.match(r"^The target block.*$", response) is not None:
            raise ValueError("Invalid coordinate target")
        if re.match(r"^No entity was.*$", response) is not None:
            raise ValueError("Invalid selector")
        if re.match(r"^Expected whitespace.*$", response) is not None:
            raise ValueError("Invalid namespace")
    
    def modifyvalue(self, path, method, value):
        methods = ["append", "insert", "merge", "prepend", "set"]

        if not method in methods:
            raise ValueError("Invalid method")
        
        cmd = "data modify storage " + self.namespace + " " + path + " " + method + " value " + value
        response = self.mrcon.run(cmd)

        if re.match(r"^Invalid NBT.*$", response) is not None:
            raise ValueError("Invalid path")
        if re.match(r"^Unknown or incomplete command.*$", response) is not None:
            raise ValueError("Incomplete command")
        if re.match(r"^Expected whitespace.*$", response) is not None:
            raise ValueError("Invalid namespace")


class MinecraftScoreboard:
    def __init__(self, mrcon, objective, ensure_created, criteria, display_name):
        self.mrcon = mrcon
        self.objective = objective

        if ensure_created:
            query = "scoreboard objectives add " + objective + " " + criteria
            if not display_name == "":
                query + " " + display_name
            mrcon.run(query)
    
    def get(self, target):
        cmd = "scoreboard players get " + target + " " + self.objective
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
        elif re.match(r"^.*none is set$", response) is not None:
            return None

        value = int(response.split(" ")[2])
        return int(value)
    
    def set(self, target, value:int):
        cmd = "scoreboard players set " + target + " " + self.objective + " " + str(value)
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
        elif re.match(r"^Invalid integer.*$", response) is not None:
            raise ValueError("Invalid integer")
    
    def add(self, target, value:int):
        cmd = "scoreboard players add " + target + " " + self.objective + " " + str(value)
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
        elif re.match(r"^Invalid integer.*$", response) is not None:
            raise ValueError("Invalid integer")
    
    def remove(self, target, value:int):
        cmd = "scoreboard players remove " + target + " " + self.objective + " " + str(value)
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
        elif re.match(r"^Invalid integer.*$", response) is not None:
            raise ValueError("Invalid integer")
    
    def enable(self, target, trigger):
        cmd = "scoreboard players enable " + target + " " + trigger
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
    
    def list(self, target):
        cmd = "scoreboard players list " + target
        response = self.mrcon.run(cmd)

        if re.match(r"^.*has no scores to show$", response) is not None:
            return {}
        
        liszt = re.split(r"(?<=[0-9])(?=\[)", response)
        pairs = {}
        for item in liszt:
            name = re.findall(r"(?<=\[)[^\]]+(?=\])", item)[0]
            value = int(re.findall(r"(?<=: )-?[0-9]+$", item)[0])
            pairs[name] = value

        return pairs
    
    def operation(self, target, operation, op_target, op_objective):
        accepted_ops = ["%=", "*=", "+=", "-=", "/=", "<", "=", ">", "><"]
        if not operation in accepted_ops:
            raise ValueError("Invalid operation '" + operation + "'")

        cmd = "scoreboard players operation " + target + " " + self.objective + " " + operation + " " + op_target + " " + op_objective
        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
    
    def reset(self, target, universal=False):
        cmd = "scoreboard players reset " + target

        if not universal:
            cmd += " " + self.objective

        response = self.mrcon.run(cmd)

        if re.match(r"^Unknown scoreboard objective.*$", response) is not None:
            raise ValueError("Invalid objective name")
            

class MinecraftRCon:
    def __init__(self, ip, port, pwd):
        self.ip = ip
        self.port = port
        self.pwd = pwd
        
        self.conn = Client(self.ip, self.port, passwd=self.pwd)
        self.conn.__enter__()
     
    def __enter__(self):
        return self.conn
 
    def __exit__(self, *args):
        print("RCon connection closed.")
        self.conn.close()

    def run(self, command):
        return self.conn.run(command)

    def get_scoreboards(self):
        cmd = "scoreboard objectives list"
        response = self.run(cmd)
        artifacts = response.split(" ")

        values = ' '.join(artifacts[4:])
        values = re.findall(r"\[[^ \]]+\]", values)

        return values
    
    def get_scoreboard(self, objective, ensure_created=False, criteria="dummy", display_name=""):
        return MinecraftScoreboard(self, objective, ensure_created, criteria, display_name)
    
    def get_storage(self, namespace):
        return MinecraftStorage(self, namespace)

