import argparse
import collections
import os
import tempfile
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    parser.add_argument('--val')
    args = parser.parse_args()
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    storage_dict = collections.OrderedDict()
    if os.path.exists(storage_path):
        with open(storage_path, 'r') as f:
            storage_dict = collections.OrderedDict(json.load(f))
    else:
        with open(storage_path, 'w') as f:
            json.dump(storage_dict, f)

    if args.key and args.val:
        if args.key not in storage_dict:
            storage_dict[args.key] = []
        storage_dict[args.key].append(args.val)
    elif args.key and not args.val:
        with open(storage_path, 'r') as f:
            loaded_dict = json.load(f)
            if args.key in storage_dict.keys():
                print(', '.join(storage_dict.get(args.key)))
            else:
                print(None)

    with open(storage_path, 'w') as f:
        json.dump(storage_dict, f)
