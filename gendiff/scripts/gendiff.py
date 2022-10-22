#!/usr/bin/env python3#!/usr/bin/env python3
import argparse
import json


def sort_func(element):
    dict = {' ' : '0', '-' : '1', '+' : '2'}
    res = element[4:element.index(':')]+dict[element[2]]
    return res

def generate_diff(file_path1, file_path2):
    file1_dict = json.load(open(file_path1))
    file2_dict = json.load(open(file_path2))

    key_set1 = set(file1_dict.keys())
    key_set2 = set(file2_dict.keys())
    result = []
    for key in key_set1:
        if key in key_set2:
            result.extend(get_line_to_append(key, file1_dict, file2_dict))
            key_set2.remove(key)
        else:
            result.append(f'  - {key}: {file1_dict[key]}')

    for key in key_set2:
        result.append(f'  + {key}: {file2_dict[key]}')

    result.sort(key = sort_func)
    result.insert(0, '{')
    result.append('}')
    return '\n'.join(result)
    
def get_line_to_append(key, file1_dict, file2_dict):
    if file1_dict[key] == file2_dict[key]:
        return [f'    {key}: {file1_dict[key]}']
    else:
        return [f'  - {key}: {file1_dict[key]}', f'  + {key}: {file2_dict[key]}']


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format', type=str, help='set format of output')
    args = parser.parse_args()
    res = generate_diff(args.first_file, args.second_file)
    print(res)

if __name__ == '__main__':
    main()