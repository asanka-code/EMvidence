import argparse

parser = argparse.ArgumentParser(description='Commandline interface of the EMvidence framework.')

# the action that needs to be done
parser.add_argument('-a', '--action', metavar='action', choices=['c', 'v', 'a'],
                    nargs=1, default=None, help='The action that needs to be done c:capture, v: visualize, a: analyze.')


#parser.add_argument('integers', metavar='integers', type=int, nargs='+', help='A set of integers for addition')

# Take the age as an integer
parser.add_argument('--age', metavar='age', type=int, nargs='?', help='The age as an integer')

# Take the name as a string by default
parser.add_argument('--name', metavar='name', nargs='?', help='The name as a string')

args = parser.parse_args()


#print(args.integers)

if args.action is None:
    parser.print_help()
else:
    action = args.action[0]
    if action == 'c':
        print("Capturing data...")
    elif action == 'a':
        print("Analyzing data...")
    elif action == 'v':
        print("Visualizing data...")

    print(args.age)
    print(args.name)