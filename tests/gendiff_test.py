from gendiff.scripts.gendiff import get_diffs_of_dicts
from gendiff.scripts.gendiff import get_dictionary_from_file

def test1():
    dict1 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict2 = {'timeout': 20, 'verbose': True, 'host': 'hexlet.io'}
    assert get_diffs_of_dicts(dict1, dict2)=='{\n  - follow: False\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: True\n}'

def test2():
    dict2 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict1 = {}
    assert get_diffs_of_dicts(dict1, dict2)=='{\n  + follow: False\n  + host: hexlet.io\n  + proxy: 123.234.53.22\n  + timeout: 50\n}'
    
def test3():
    dict1 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict2 = {}
    assert get_diffs_of_dicts(dict1, dict2)=='{\n  - follow: False\n  - host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n}'
    
def test4():
    file1_dict = get_dictionary_from_file('tests/file1.json')
    assert file1_dict=={'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}