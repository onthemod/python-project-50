#!/usr/bin/env python3#!/usr/bin/env python3
import argparse
import json
import yaml


def generate_diff(file_path1, file_path2):
    diff_tree = generate_diff_tree(file_path1, file_path2)
    return stringify(diff_tree)


def generate_diff_tree(file_path1, file_path2):
    file1_dict = get_dictionary_from_file(file_path1)
    file2_dict = get_dictionary_from_file(file_path2)
    return get_diff_tree_of_dicts(file1_dict, file2_dict)


def get_diff_tree_of_dicts(dict1, dict2):
    dict1 = cut_null_values(dict1)
    dict2 = cut_null_values(dict2)
    result = []
    for key in get_keys(dict1, dict2):
        diff_strings = get_diff_tuple_list(
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


def get_diff_tuple_list(key, value1, value2):
    if value1 is None:
        return [get_added_pair_tuple(key, value2)]
    if value2 is None:
        return [get_removed_pair_tuple(key, value1)]
    if value1 == value2:
        return [get_non_changed_pair_tuple(key, value1)]
    if isinstance(value1, dict) and isinstance(value2, dict):
        return [get_non_changed_pair_tuple(
            key, get_diff_tree_of_dicts(value1, value2))]
    return [get_removed_pair_tuple(key, value1),
            get_added_pair_tuple(key, value2)]


def get_added_pair_tuple(key, value):
    value = get_dict_list(value)
    return ('+', key, value)


def get_removed_pair_tuple(key, value):
    value = get_dict_list(value)
    return ('-', key, value)


def get_non_changed_pair_tuple(key, value):
    value = get_dict_list(value)
    return (' ', key, value)


def stringify(lst, inset=0):
    res = '{\n'
    spacing = inset * 4 * ' '
    for item in lst:
        res = res + spacing + string_of_item(item, inset)
    res = res + spacing + '}'
    return res


def string_of_item(item, inset):
    s, k, v = item
    v = get_value_string(v, inset)
    return f'  {s} {k}: {v}\n'


def get_value_string(val, inset=0):
    if isinstance(val, list):
        return stringify(val, inset + 1)
    return val


def get_dict_list(d):
    if isinstance(d, dict):
        res = []
        for k, v in d.items():
            res.append(get_non_changed_pair_tuple(k, v))
        return res
    return d


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
