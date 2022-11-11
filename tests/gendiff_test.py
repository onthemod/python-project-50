from gendiff.scripts.gendiff import get_diffs_of_dicts
from gendiff.scripts.gendiff import get_dictionary_from_file
from gendiff.scripts.gendiff import generate_diff
import pytest

@pytest.fixture
def diff1():
    return '{\n  - follow: False\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: True\n}'
    

@pytest.fixture
def dictionary1():
    return {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}

def test1(diff1):
    dict1 = {'host': 'hexlet.io', 'timeout': 50, 'proxy': '123.234.53.22', 'follow': False}
    dict2 = {'timeout': 20, 'verbose': True, 'host': 'hexlet.io'}
    assert get_diffs_of_dicts(dict1, dict2)==diff1

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
    
    
def test_yaml(dictionary1):
    file1_dict = get_dictionary_from_file('tests/file1.yaml')
    assert file1_dict==dictionary1
    

def test_yml(dictionary1):
    file1_dict = get_dictionary_from_file('tests/file1.yml')
    assert file1_dict==dictionary1
    

def test5():
    diff = '{\n  - follow: False\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: True\n}'
    assert generate_diff('tests/file1.json','tests/file2.json')==diff
