#! /usr/bin/env python3

import argparse
import json
import requests
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='server host', default='192.35.222.130')
    parser.add_argument('--port', help='server port', default=5555)
    parser.add_argument('--status', help='get status', action='store_true')
    parser.add_argument('--challenge', help='challenge name')
    args = parser.parse_args()

    if args.status:
        url = f'http://{args.host}:{args.port}/api/status'
        r = requests.get(url=url)
        # pretty print r.json()
        print(json.dumps(r.json(), indent=4))
        sys.exit(0)
    elif not args.challenge:
        parser.print_help()
        sys.exit(1)

    # send a GET request with args token and challenge name to /api/submit_token with timeout of 60 seconds
    try:
        token = input('Enter your token to connect to the challenge: ')

        print('Waiting for server response...')

        if not token or len(token) != 64 or not all(c in '0123456789abcdef' for c in token):
            print('Request rejected. Invalid token')
            sys.exit(1)

        url = f'http://{args.host}:{args.port}/api/submit_token'
        params = {'token': token, 'challenge': args.challenge}
        r = requests.get(url=url, params=params, timeout=60)
        # accepted if response is 200 and json['accepted'] is True
        if r.status_code == 200:
            print(f'{r.json()["reason"]}')
            if r.json()['accepted'] is True:
                sys.exit(0)
            else:
                sys.exit(1)
    except Exception as e:
        pass

    # if we get here, exit with error
    print('\nSomething went wrong, please try again. If the problem persists, please contact the admins.')
    sys.exit(1)

if __name__ == '__main__':
    main()

