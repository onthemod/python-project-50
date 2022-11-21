#!/usr/bin/env python3#!/usr/bin/env python3
import argparse
import json
import yaml
import sys
sys.path.insert(0, '..')
sys.path.insert(0, './gendiff')
from treenode import create_added_node
from treenode import create_removed_node
from treenode import create_nonchanged_node
from treenode import create_updated_node
import formaters.stylish as stylish
import formaters.plain as plain


def generate_diff(file_path1, file_path2, formater=stylish):
    diff_tree = generate_diff_tree(file_path1, file_path2)
    return formater.stringify(diff_tree)


def generate_diff_tree(file_path1, file_path2):
    file1_dict = get_dictionary_from_file(file_path1)
    file2_dict = get_dictionary_from_file(file_path2)
    return get_diff_tree(file1_dict, file2_dict)


def get_diff_tree(dict1, dict2):
    dict1 = cut_null_values(dict1)
    dict2 = cut_null_values(dict2)
    result = []
    for key in get_keys(dict1, dict2):
        diff_strings = get_diff_child_tree(
            key, dict1.get(key), dict2.get(key))
        result.extend(diff_strings)
    return result


def get_dictionary_from_file(file_path):
    o = open(file_path)
    if file_path[-4:] == 'json':
        return json.load(o)
    if file_path[-4:] == 'yaml' or file_path[-3:] == 'yml':
        return yaml.safe_load(o)


def cut_null_values(dictionary):
    result = {}
    for k, v in dictionary.items():
        if v is None:
            v = 'null'
        result[k] = v
    return result


def get_keys(dict1, dict2):
    keyset = set()
    keyset.update(dict1.keys())
    keyset.update(dict2.keys())
    keylist = list(keyset)
    keylist.sort()
    return keylist


def get_diff_child_tree(key, value1, value2):
    if value1 is None:
        return [create_added_node(key, value2)]
    if value2 is None:
        return [create_removed_node(key, value1)]
    if value1 == value2:
        return [create_nonchanged_node(key, value1)]
    if isinstance(value1, dict) and isinstance(value2, dict):
        return [create_nonchanged_node(
            key, get_diff_tree(value1, value2))]
    return [create_updated_node(key, value1, value2)]


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration '
                                     ' files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', type=str, help='set format of output')
    args = parser.parse_args()
    formater = stylish
    if args.format == 'plain':
        formater = plain
    res = generate_diff(args.first_file, args.second_file, formater)
    print(res)


if __name__ == '__main__':
    main()
