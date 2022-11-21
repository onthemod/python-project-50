def create_added_node(key, value):
    value = split_dict_value(value)
    return ('+', key, value)


def create_removed_node(key, value):
    value = split_dict_value(value)
    return ('-', key, value)


def create_nonchanged_node(key, value):
    value = split_dict_value(value)
    return (' ', key, value)


def create_updated_node(key, value1, value2):
    value1 = split_dict_value(value1)
    value2 = split_dict_value(value2)
    return ('-+', key, value1, value2)

    
def is_added(node):
    return node[0] == '+'


def is_removed(node):
    return node[0] == '-'


def is_non_changed(node):
    return node[0] == ' '


def is_updated(node):
    return node[0] == '-+'


def get_key(node):
    return node[1]
    
    
def get_value(node):
    if len(node) == 4:
        return (node[2], node[3])
    return node[2]


def split_dict_value(value):
    if isinstance(value, dict):
        res = []
        for k, v in value.items():
            res.append(create_nonchanged_node(k, v))
        return res
    return value
