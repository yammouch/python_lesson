import argparse

parser = argparse.ArgumentParser(description='a lesson of argparse')
parser.add_argument('--lr', type=float, default=0.1,
                    help='learning rate')
parser.add_argument('--seed', type=int, default=1,
                    help='seed of random value')
args = parser.parse_args()

print(args)
