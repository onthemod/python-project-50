from gendiff import get_diff_for_key

def print_d():
    key = 'key'
    dict1 = {'ikey1': 'ival1', 'ikey2':'ival2'}
    dict2 = {'ikey1': 'ival2', 'ikey3':'ival2i'}
    dict_diffs = get_diff_for_key(key, dict1, dict2)
    for a in dict_diffs:
        print(a+'\n')


print_d()
