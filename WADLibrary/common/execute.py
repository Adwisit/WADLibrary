import requests
import json
from .errors import Error


def get(url, params=None, catch_error=True, **kwargs):
    return analyse(requests.get(url, params, **kwargs), catch_error)


def post(url, data=None, json=None, catch_error=True, **kwargs):
    return analyse(requests.post(url, data, json, **kwargs), catch_error)


def delete(url, catch_error=True, **kwargs):
    return analyse(requests.delete(url, **kwargs), catch_error)


def analyse(res, catch_error):
    json_obj = json.loads(res.text)
    if json_obj['status'] == 0 or not catch_error:
        return res
    else:
        value = '------------------------------------ERROR-------------------------------------\n' +\
                'Status: ' + str(json_obj['status']) + ', ' + json_obj['value']['error'] + '\n' +\
                json_obj['value']['message'] + '\n' +\
                '------------------------------------------------------------------------------'
        raise Error(value)
