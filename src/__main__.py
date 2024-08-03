import argparse
from pprint import pprint

from src.data_loading import load_csv
from src.quine_mckluskey import minimize_dataset


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="QuineMcLuskey",
        description="Small command line utility for simplifying boolean tables",
        epilog=r"For more information see the readme at https://github.com/MalinkyZubr/QuineMcKluskey"
    )
    parser.add_argument('csv_path', "Absolute path to csv file containing raw boolean conditions")
    parser.add_argument("-t", "--time", "Track and print execution time at completion")
    parser.add_argument("-d", "--distributive", "Try and simplify output expressions using the distributive property")
    parser.add_argument("-l", "--locator", "Identify all identical tokens between all generated expressions. Identical tokens can be reduced to a single gate during circuit design")
    
    pprint(minimize_dataset(load_csv(r"/home/malinkyzubr/Desktop/InterruptExpander/hardware/logic/scripts/TRUTH_TABLE3.csv")))