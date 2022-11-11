#!/usr/bin/env python3#!/usr/bin/env python3
import argparse
import json
import yaml


def generate_diff(file_path1, file_path2):
    file1_dict = get_dictionary_from_file(file_path1)
    file2_dict = get_dictionary_from_file(file_path2)
    print(file1_dict)
    return get_diffs_of_dicts(file1_dict, file2_dict)


def get_dictionary_from_file(file_path):
    o = open(file_path)
    if file_path[-4:] == 'json':
        return json.load(o)
    if file_path[-4:] == 'yaml' or file_path[-3:] == 'yml':
        return yaml.safe_load(o)


def get_keys(dict1, dict2):
    keyset = set()
    keyset.update(dict1.keys())
    keyset.update(dict2.keys())
    keylist = list(keyset)
    keylist.sort()
    return keylist


def get_diff_for_key(key, value1, value2):
    if value1 is None:
        return [wrap_added_pair(key, value2)]
    if value2 is None:
        return [wrap_removed_pair(key, value1)]
    if value1 == value2:
        return [wrap_not_changed_pair(key, value1)]
    return [wrap_removed_pair(key, value1), wrap_added_pair(key, value2)]


def wrap_added_pair(key, value):
    return f'  + {key}: {value}'


def wrap_removed_pair(key, value):
    return f'  - {key}: {value}'


def wrap_not_changed_pair(key, value):
    return f'    {key}: {value}'


def get_diffs_of_dicts_list(dict1, dict2):
    result = []
    for key in get_keys(dict1, dict2):
        diff_strings = get_diff_for_key(key, dict1.get(key), dict2.get(key))
        result.extend(diff_strings)
    return result


def get_diffs_of_dicts(dict1, dict2):
    diff_list = get_diffs_of_dicts_list(dict1, dict2)
    diff_list.insert(0, '{')
    diff_list.append('}')
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
