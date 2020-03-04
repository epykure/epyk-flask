import requests, json


input = {'function': 'foo', 'module': 'my_tests', 'path': r'D:\Experiments\test_python', 'extra_params': {'a': 1, 'b': 2}}
input2 = {'function': 'bar', 'module': 'my_tests', 'path': r'D:\Experiments\test_python', 'extra_params': {'a': 1, 'b': 2, 'test': 'toto'}}
input3 = {'function': 'spam', 'module': 'my_tests', 'path': r'D:\Experiments\test_python', 'extra_params': {'args': [1,2, 3, 4,5] , 'kwargs': {'test': 'tata', 'tet': 'cochon'}}}
input4 = {'function': 'alot', 'module': 'my_tests', 'path': r'D:\Experiments\test_python', 'extra_params': {'a': 1, 'b': 2, 'args': [1,2, 3, 4,5] , 'kwargs': {'test': 'tata', 'tet': 'cochon'}, 'test': 'toto'}}
url = 'http://127.0.0.1:5000/data/get'

print(requests.post(url, data=json.dumps(input)).text)
print(requests.post(url, data=json.dumps(input2)).text)
print(requests.post(url, data=json.dumps(input3)).text)
print(requests.post(url, data=json.dumps(input4)).text)