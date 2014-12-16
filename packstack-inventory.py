#!/usr/bin/python

import os
import sys
import argparse
from ConfigParser import ConfigParser
import json


def get_inventory(cfg):
    inv = {}

    for host in ['controller', 'amqp', 'storage',
                 'mariadb', 'mongodb']:
        inv[host] = {
            'hosts': [cfg.get('general',
                              'config_{host}_host'.format(host=host))],
        }

    for host in ['network', 'compute']:
        inv[host] = {
            'hosts': cfg.get('general',
                              'config_{host}_hosts'.format(
                                  host=host)).split(','),
        }

    return inv

def get_meta(cfg):
    return dict(cfg.items('general'))


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--answer-file',
                   default=os.getenv('PACKSTACK_ANSWER_FILE',
                                     'answers.txt'))
    p.add_argument('--host')
    p.add_argument('--list',
                   action='store_true')
    return p.parse_args()

def main():
    args = parse_args()
    cfg = ConfigParser()
    cfg.read(args.answer_file)

    if args.list:
        inv = get_inventory(cfg)
        print json.dumps(inv, indent=2)
    elif args.host:
        meta = get_meta(cfg)
        print json.dumps(meta, indent=2)

if __name__ == '__main__':
    main()


