import argparse
from argparse import Namespace
import toml

def parse_args():
    parser = argparse.ArgumentParser(description='read')

    parser.add_argument('config_path', type=str, help='location of the conifg to run')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args() # get the config path

    with open(args.config_path) as f:
        run = Namespace(**toml.load(f))
        # import your main function
        # run the main function with the args
