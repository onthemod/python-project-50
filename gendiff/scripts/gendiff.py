#!/usr/bin/env python3#!/usr/bin/env python3
import argparse
import json
import yaml


def generate_diff(file_path1, file_path2):
    file1_dict = get_dictionary_from_file(file_path1)
    file2_dict = get_dictionary_from_file(file_path2)
    return get_diffs_of_dicts(file1_dict, file2_dict)


def get_dictionary_from_file(file_path):
    o = open(file_path)
    if file_path[-4:] == 'json':
        return json.load(o)
    if file_path[-4:] == 'yaml' or file_path[-3:] == 'yml':
        return yaml.safe_load(o)
        
        
def cut_null_values(dictionary):
    result = {}
    for k,v in dictionary.items():
        if v is None:
            print("isNone")
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


def get_diff_for_key(key, value1, value2, inset):
    if value1 is None:
        return [wrap_added_pair(key, value2, inset)]
    if value2 is None:
        return [wrap_removed_pair(key, value1, inset)]
    if value1 == value2:
        return [wrap_not_changed_pair(key, value1, inset)]
    if isinstance(value1, dict) and isinstance(value2, dict):
        return [wrap_not_changed_pair(key, get_diffs_of_dicts_list(value1, value2, inset + 1), inset)]
    return [wrap_removed_pair(key, value1, inset), wrap_added_pair(key, value2, inset)]


def added_pair_key_prefix(key):
    return f'  + {key}: '
    
    
def removed_pair_key_prefix(key):
    return f'  - {key}: '
    
    
def not_changed_pair_key_prefix(key):
    return f'    {key}: '
    

def suffix(value, inset=0):
    if isinstance(value, list):
        return '\n'.join(value)
    if isinstance(value, dict):
        return get_dictionary_string(value, inset+1);
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def wrap_added_pair(key, value, inset):
    return ' ' * 4 * inset + added_pair_key_prefix(key) + suffix(value, inset)
    
    
def wrap_removed_pair(key, value, inset):
    return ' ' * 4 * inset + removed_pair_key_prefix(key) + suffix(value, inset)
    
    
def wrap_not_changed_pair(key, value, inset):
    return ' ' * 4 * inset + not_changed_pair_key_prefix(key) + suffix(value, inset)


def get_dictionary_string(d, inset):
    stringlist = ['{']
    for key, value in d.items():
        stringlist.append( wrap_not_changed_pair(key, value, inset))
    stringlist.append(inset * 4 * ' ' + '}')
    return '\n'.join(stringlist)


def get_string_of_value(value):
    if isinstance(value, dict):
        res = "{"
        for k, v in value.items():
            res=res+'\n'+ '    '+k+': '+v
        res = res + '\n}'


def get_diffs_of_dicts_list(dict1, dict2, inset=0):
    dict1 = cut_null_values(dict1)
    dict2 = cut_null_values(dict2)
    result = []
    for key in get_keys(dict1, dict2):
        diff_strings = get_diff_for_key(key, dict1.get(key), dict2.get(key), inset)
        result.extend(diff_strings)
    result.insert(0, '{')
    result.append(inset * 4 * ' ' + '}') 
    return result


def get_diffs_of_dicts(dict1, dict2):
    diff_list = get_diffs_of_dicts_list(dict1, dict2)
    return '\n'.join(diff_list)


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration '
                                     ' files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', type=str, help='set format of output')
    args = parser.parse_args()
    res = generate_diff(args.first_file, args.second_file)
    print(res)


if __name__ == '__main__':
    main()
