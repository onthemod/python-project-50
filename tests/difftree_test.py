from gendiff.scripts.gendiff import generate_diff_tree
from gendiff.scripts.gendiff import stringify


def test_of_dict():
    test_list = [(' ', 'common', [('+', 'follow', False), (' ', 'setting1', 'Value 1'),
                ('-', 'setting2', 200), ('-', 'setting3', True), ('+', 'setting3', 'null'),
                ('+', 'setting4', 'blah blah'), ('+', 'setting5', [( ' ', 'key5', 'value5')]),
                ( ' ', 'setting6', [(' ', 'doge', [( '-', 'wow', ''), ('+', 'wow', 'so much')]),
                (' ', 'key', 'value'),('+',  'ops', 'vops')])]),(' ', 'group1', [('-', 'baz', 'bas'),
                ( '+',  'baz', 'bars'), ( ' ', 'foo', 'bar'), ( '-',  'nest', [( ' ', 'key', 'value')]), 
                ( '+',  'nest', 'str')])]
    res = generate_diff_tree('tests/nested_short1.json', 'tests/nested_short2.json')
    print(res)
    print('-----------------------------------')
    print(test_list)
    assert test_list == res
    
    
def test_of_str():
    test_tree = [(' ', 'key1', 'value1'), ('+', 'key2', [(' ', 'key3', 'value2')])]
    s = '{\n    key1: value1\n  + key2: {\n        key3: value2\n    }\n}'
    print(stringify(test_tree))
    assert stringify(test_tree) == s
