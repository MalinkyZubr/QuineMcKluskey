import sys
import cProfile
sys.path.append("/home/malinkyzubr/Desktop/InterruptExpander/hardware/logic")

from scripts.QuineMcluskey import *

cProfile.run('pprint(minimize_dataset(load_csv(r"/home/malinkyzubr/Desktop/InterruptExpander/hardware/logic/scripts/TRUTH_TABLE2.csv")))')