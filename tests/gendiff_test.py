from gendiff.scripts.gendiff import get_diffs_of_dicts
from gendiff.scripts.gendiff import get_dictionary_from_file
from gendiff.scripts.gendiff import generate_diff
from gendiff.scripts.gendiff import get_dictionary_string
import pytest

@pytest.fixture
def diff1():
    return '{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}'
    

@pytest.fixture
def dictionary1():
    return {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    
@pytest.fixture
def dict_string_inset_1():
    return "{\n        host: hexlet.io\n        timeout: 50\n        proxy: 123.234.53.22\n        follow: false\n    }"
    
def test_dict_string(dictionary1,dict_string_inset_1):
    print(dict_string_inset_1)
    print(get_dictionary_string({'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}, 1))
    assert get_dictionary_string({'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}, 1) == dict_string_inset_1

def test1(diff1):
    dict1 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict2 = {'timeout': 20, 'verbose': True, 'host': 'hexlet.io'}
    assert get_diffs_of_dicts(dict1, dict2)==diff1

def test2():
    dict2 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict1 = {}
    assert get_diffs_of_dicts(dict1, dict2)=='{\n  + follow: false\n  + host: hexlet.io\n  + proxy: 123.234.53.22\n  + timeout: 50\n}'
    
def test3():
    dict1 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict2 = {}
    assert get_diffs_of_dicts(dict1, dict2)=='{\n  - follow: false\n  - host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n}'
    
    
def test_dict_appeared():
    dict1 = {}
    dict2 = {'key1': {'timeout': 50, 'proxy': '123.234.53.22'}, 'key2': 'value'}
    assert get_diffs_of_dicts(dict1, dict2)=='{\n  + key1: {\n        timeout: 50\n        proxy: 123.234.53.22\n    }\n  + key2: value\n}'


def test4():
    file1_dict = get_dictionary_from_file('tests/file1.json')
    assert file1_dict=={'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    
    
def test_yaml(dictionary1):
    file1_dict = get_dictionary_from_file('tests/file1.yaml')
    assert file1_dict==dictionary1
    

def test_yml(dictionary1):
    file1_dict = get_dictionary_from_file('tests/file1.yml')
    assert file1_dict==dictionary1
    

def test5():
    diff = '{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}'
    assert generate_diff('tests/file1.json','tests/file2.json')==diff
    
def test_nested():
    f = open('tests/result.txt', 'r')
    diff_strig = generate_diff('tests/nested1.json','tests/nested2.json')
    d = zip(diff_strig.split('\n'), f)
    for k,v in d:
        assert k == v or k + '\n' == v
