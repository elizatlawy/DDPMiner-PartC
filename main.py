from DDPMiner import DDPMine
from fptree import FPTree
from TransactionDatabase import TransactionDatabase
from optparse import OptionParser
import data_preprocess


def run_ddpmine():
    # Just some placeholder data
    miner = DDPMine(["a", "b"])
    miner.mine()




if __name__ == "__main__":
    ########## RUN FORM Terminal  ##############
    # usage = "usage: %prog [options] filename"
    # parser = OptionParser(usage)
    # parser.add_option("-d", "--debug",
    #                   action="store_true", dest="debug")
    #
    # (options, args) = parser.parse_args()

    # if len(args) != 3:
    #     parser.error("You must give the filename, label support symbol, and minimum support.")

    # print("Mining from file %s..." % args[0])
    # print("Using label support symbol %s..." % args[1])
    # print("Using support of %s..." % args[2])
    # database = TransactionDatabase.loadFromFile(args[0], args[1], int(float(args[2])))

    ######### RUN FORM FILE  ##############
    print("Creating DB..")
    database = TransactionDatabase.loadFromFile("bio_data/10_only_trans.csv", "1", 9)
    print("hey")



    miner = DDPMine(debug=True)
    print("Starat mining..")
    miner.mine(database, 9)
