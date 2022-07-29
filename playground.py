import argparse

def stringOnly(x):
    try:
        int(x)
    except ValueError:
        return x
    raise argparse.ArgumentTypeError('only strings fool')

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('--hello', type=stringOnly, required=True,
                    help='Please provide string')
a = parser.parse_args()



print('yep')
print(type(a.hello))
print(a)

import ast