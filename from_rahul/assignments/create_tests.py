import os
import sys
from shutil import rmtree
import argparse
from importlib import import_module

# python create_tests.py 04_curry_price -p

def print_row(file, data):
    if isinstance(data, tuple):
        data = list(data)
    if isinstance(data, list):
        c = ' '.join([str(x) for x in data])
        file.write(f"{c}\n")
    else:
        file.write(f"{data}\n")


def print_test(file, data):
    if isinstance(data, list):
        for row in data:
            print_row(file, row)
    else:
        print_row(file, data)


def create_tests(folder, tests):
    i_dir = os.path.join(folder, "input")
    o_dir = os.path.join(folder, "output")

    os.makedirs(i_dir, exist_ok=True)
    os.makedirs(o_dir, exist_ok=True)

    for c, (i, o) in enumerate(tests):
        with open(os.path.join(i_dir, f"input{c:03d}.txt"), 'w') as in_file:
            print_test(in_file, i)
        with open(os.path.join(o_dir, f"output{c:03d}.txt"), 'w') as out_file:
            print_test(out_file, o)


def get_args():
    parser = argparse.ArgumentParser(
        description='This will generate input-output files for the python assignments')
    parser.add_argument('name',
                        help='this will read the given assignment name')
    media = os.path.join(os.path.dirname(__file__), "..", "..", "media", "assignments")
    parser.add_argument('-o', '--out', default=media,
                        help='use this dir as output')
    parser.add_argument('-p', '--print', action='store_true')
    return parser.parse_args()


def main():
    args = get_args()
    # filepath = os.path.join(os.path.dirname(__file__), args.name)
    # sys.meta_path.insert(0, os.path.dirname(__file__))
    tests = import_module(args.name).main()
    print(f"{len(tests)} tests loaded")
    if args.print:
        print(tests)
    test_dir = os.path.join(args.out, args.name)
    if os.path.isdir(test_dir):
        rmtree(test_dir)
    create_tests(test_dir, tests)

if __name__ == '__main__':
    main()
