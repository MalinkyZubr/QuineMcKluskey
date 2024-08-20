import argparse
from pprint import pprint

import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loading import load_csv
from quine_mckluskey import minimize_dataset


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="QuineMcLuskey",
        description="Small command line utility for simplifying boolean tables",
        epilog=r"For more information see the readme at https://github.com/MalinkyZubr/QuineMcKluskey"
    )
    parser.add_argument('csv_path', help="Absolute path to csv file containing raw boolean conditions")
    parser.add_argument("-t", "--time", help="Track and print execution time at completion")
    parser.add_argument("-d", "--distributive", help="Try and simplify output expressions using the distributive property")
    parser.add_argument("-l", "--locator", help="Identify all identical tokens between all generated expressions. Identical tokens can be reduced to a single gate during circuit design")
    
    args = vars(parser.parse_args())
    
    pprint(minimize_dataset(load_csv(args["csv_path"])))