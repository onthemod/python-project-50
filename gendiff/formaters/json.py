from treenode import is_updated
import json

def stringify(lst):
    with open("data_file.json", "w") as write_file:
        json.dump(lst, write_file)
