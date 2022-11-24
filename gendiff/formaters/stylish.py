from gendiff.treenode import is_updated

def stringify(lst, inset=0):
    res = '{\n'
    spacing = inset * 4 * ' '
    for item in lst:
        res = res + spacing + string_of_item(item, inset)
    res = res + spacing + '}'
    return res


def string_of_item(item, inset):
    if is_updated(item):
        result = string_of_updated_item(item, inset)
    else:
        result = string_of_single_item(item, inset)
    return result 


def string_of_updated_item(item, inset):
    _, k, v1, v2 = item
    v1 = get_value_string(v1, inset)
    v2 = get_value_string(v2, inset)
    spacing = inset * 4 * ' '
    return f'  - {k}: {v1}\n {spacing} + {k}: {v2}\n'


def string_of_single_item(item, inset):     
    s, k, v = item
    v = get_value_string(v, inset)
    return f'  {s} {k}: {v}\n'

def get_value_string(val, inset=0):
    if isinstance(val, list):
        return stringify(val, inset + 1)
    return val
