import json
import random


def set_cookie_response(cookie_value, redirect):
    response = {
        'status': '302',
        'statusDescription': 'Found',
        'headers': {
            'location': [{
                'key': 'Location',
                'value': redirect
            }],
            'set-cookie': [{
                'key': 'Set-Cookie',
                'value': cookie_value
            }]
        }
    }
    return response


def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    headers = request['headers']
    uri = request['uri']

    cookie_a = 'app-version=A'
    cookie_b = 'app-version=B'
    path_a = '/version-a.html'
    path_b = '/version-b.html'

    experiment_uri = ""

    for cookie in headers.get('cookie', []):
        if cookie_a in cookie['value']:
            print("Experiment A cookie found")
            experiment_uri = path_a
            break
        elif cookie_b in cookie['value']:
            print("Experiment B cookie found")
            experiment_uri = path_b
            break

    if not experiment_uri:
        print("Experiment cookie has not been found. Throwing dice...")
        if random.random() < 0.5:
            return set_cookie_response(cookie_a, uri)
        else:
            return set_cookie_response(cookie_b, uri)
            
    request['uri'] = experiment_uri

    print(f"Request uri set to {experiment_uri}")
    return request
