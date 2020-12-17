import time
from DDPMiner import DDPMine
from TransactionDatabase import TransactionDatabase
import data_preprocess
import generator
import json
from matplotlib import pyplot as plt


def lines_that_contain(string, fp):
    return [line for line in fp if string in line]


def generate_report():
    """
    Function that generate detailed report from the DDPminer results in the follownf Form:
    ++++++++++++++++  Results report for minSup = 5 +++++++++++++++
    Results for FreqItem: [list of the freqItems]
    IG of FreqItem:  0.961236604722876
    Cogs info form COG_INFO_TABLE if exist:
    Number of appearances in Human Bacteria: int number
    percentage of appearances in Human Bacteria: %
    Number of appearances in Plant Bacteria: 2
    percentage of appearances in Plant Bacteria: %
    """
    all_results_file = open("all_results_with_minSup.json", "r")
    all_results_list = json.load(all_results_file)
    Human_total_trans_in_db = 252
    Plant_total_trans_in_db = 72
    outputFile = open("Results/Final_Report.txt", 'a+')
    for results in all_results_list:
        outputFile.write("++++++++++++++++  Results report for minSup = " + str(results[0]) + " +++++++++++++++\n")
        outputFile.write("Total Number of itemSets found = " + str(len(results[1])) + "\n")
        for freqItem in results[1]:
            appearances_in_Humnan = 0
            appearances_in_Plant = 0
            transactions_file = open("bio_data/United_unsorted_trans.csv", 'r')
            for line in transactions_file:
                all_found = True
                for cog in freqItem[0]:
                    if cog not in line:
                        all_found = False
                        break
                if all_found:
                    if line[-2:-1] == '1':
                        appearances_in_Humnan += 1
                    else:
                        appearances_in_Plant += 1
            percentage_in_human_bac = round((appearances_in_Humnan / Human_total_trans_in_db)*100, 2)
            percentage_in_plant_bac = round((appearances_in_Plant / Plant_total_trans_in_db)*100, 2)
            outputFile.write("Results for FreqItem: " + str(freqItem[0]) + '\n')
            outputFile.write("IG of FreqItem:  " + str(freqItem[1]) + '\n')
            outputFile.write("COG_INFO semantic description per each COG in the itemSet if exist:" + '\n')
            with open("bio_data/COG_INFO_TABLE.txt", "r") as fp:
                for cog in freqItem[0]:
                    info_table_results = lines_that_contain("COG" + cog, fp)
                    if len(info_table_results) == 0:
                        outputFile.write("NO Results from INFO_TABLE" + '\n')
                    else:
                        for line in info_table_results:
                            outputFile.write(line)
                    fp.seek(0)  # going back to the beginning of INFO_TABLE file
            outputFile.write("Number of occurrences in Human Bacteria genomes: " + str(appearances_in_Humnan) + '\n')
            outputFile.write("percentage of genomes that carry it in Human Bacteria genomes: " + str(percentage_in_human_bac) + "%" + '\n')
            outputFile.write("Number of occurrences in Plant Bacteria genomes: " + str(appearances_in_Plant) + '\n')
            outputFile.write("percentage of genomes that carry it in Plant Bacteria genomes: " + str(percentage_in_plant_bac) + "%" + '\n')
            outputFile.write('\n')
    outputFile.close()


def generate_running_time_graph():
    """
    This function generate Graph of Minimum Support Effect on Running Time
    X axis - Minimum Support for each rum
    Y axis -  The relative Running Time using a CPU counter
    """
    running_times_json = open("running_times.json", "r")
    running_times_list = json.load(running_times_json)
    running_times_list.reverse()
    minSups_json = open("minSup_list.json", "r")
    minSups_list = json.load(minSups_json)
    minSups_list.reverse()
    plt.plot(minSups_list, running_times_list, '--ro')
    plt.title("Minimum Support Effect on Running Time ")
    plt.xlabel("Minimum Support")
    plt.ylabel("Running Time")
    plt.savefig('Results/Running_time_graph_reversed.png')
    plt.show()


if __name__ == "__main__":
    # data_preprocess.data_to_transaction_file()
    # all_results_with_minSup = []
    # running_times = []
    # minSup_list = []
    # minSup = 324
    # while minSup >= 5:
    #     # 325 * 0.05 = 16
    #     minSup = minSup - 16  # reduce the minSup by 5% of number of genomes in the original DB for each iteration
    #     minSup_list.append(minSup)
    #     print("Creating DB.. MinSup =  ", minSup)
    #     database = TransactionDatabase.loadFromFile("bio_data/United_unsorted_trans.csv", "0", minSup)
    #     start = time.perf_counter()  # save starting time
    #     miner = DDPMine(debug=False)
    #     print("Starat mining MinSup = ", minSup)
    #     results = miner.mine(database, minSup)
    #     elapsed = time.perf_counter() - start  # calc running time for iteration
    #     running_times.append(elapsed)
    #     all_results_with_minSup.append([minSup, results])  # first item is the minSup, second is teh result
    # minSup = 4
    # while minSup > 2:
    #     minSup -= 1   # reduce the minSup by 2 for each iteration
    #     minSup_list.append(minSup)
    #     print("Creating DB.. MinSup =  ", minSup)
    #     database = TransactionDatabase.loadFromFile("bio_data/United_unsorted_trans.csv", "0", minSup)
    #     start = time.perf_counter()  # save starting time
    #     miner = DDPMine(debug=False)
    #     print("Starat mining MinSup = ", minSup)
    #     results = miner.mine(database, minSup)
    #     elapsed = time.perf_counter() - start  # calc running time for iteration
    #     running_times.append(elapsed)
    #     all_results_with_minSup.append([minSup, results])  # first item is the minSup, second is teh result
    #     # with open("Results/Results_remote.txt", 'a') as f:
    #     #     f.write("++++++++ Result for minSup = " + str(j) + "++++++++\n")
    #     #     print("number of results found: ", len(results))
    #     #     for item in results:
    #     #         f.write("%s\n" % item)
    #     #     f.write("number of results found: ")
    #     #     f.write(str(len(results)) + "\n")
    # # Dump minSup, Running Times & All results into JSON files for post-process the results
    # with open('minSup_list.json', 'w') as f:
    #     json.dump(minSup_list, f)
    # with open('running_times.json', 'w') as f:
    #     json.dump(running_times, f)
    # with open('all_results_with_minSup.json', 'w') as f:
    #     json.dump(all_results_with_minSup, f)

    #generate_report()  # generate detailed report from the DDPminer results
    generate_running_time_graph()
