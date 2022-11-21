from treenode import is_updated
from treenode import is_added
from treenode import is_removed
from treenode import get_key
from treenode import get_value

def stringify(lst):
    res = []
    for item in lst:
        res.extend(strings_of_item(item))
    return '\n'.join(res)


def strings_of_item(item, parent_key = ''):
    key = get_key(item)
    if len(parent_key)>0:
        key = parent_key + '.' + key
    value = get_value(item)
    if is_added(item):
        value = get_value_string(value)
        return [f'Property \'{key}\' was added with value: {value}']
    if is_removed(item):
        return [f'Property \'{key}\' was removed']
    if is_updated(item):
        value1 = (get_value_string(value[0]))
        value2 = (get_value_string(value[1]))
        return [f'Property \'{key}\' was updated. From {value1} to {value2}']
    if isinstance(value, list):
        res = []
        for child in value:
            res.extend(strings_of_item(child, key))
        return res
    return []


def get_value_string(val):#false true учесть
    if val == 'null':
        return 'null'
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, list):
        return '[complex value]'
    return f'\'{val}\''
