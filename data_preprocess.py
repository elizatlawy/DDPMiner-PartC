import random


def bio_data_parser():
    outputFile = open("bio_data/Plant_only_cog_words.txt", 'w+')
    Human_id_file = open('bio_data/Plant_only_bacTaxa.txt')
    for line in Human_id_file:
        Bacteria_name = line.split(";")[1]
        cog_words = open('bio_data/cog_words_bac.txt')
        for cog_line in cog_words:
            if Bacteria_name in cog_line:
                outputFile.write(cog_line)

    outputFile.close()
    Human_id_file.close()


def data_to_transaction_file():
    outputFile = open("bio_data/United_unsorted_trans.csv", 'a+')
    Human_cog_words_file = open("bio_data/Plant_only_cog_words.txt")
    last_Bacteria_name = ""
    transaction_list = []  # declare an empty list
    should_write = False
    for line in Human_cog_words_file:
        # get the Bacteria name_uid example: topobium_parvulum_DSM_20469_uid59195
        curr_Bacteria_name = line.split("#")[3]
        if last_Bacteria_name == curr_Bacteria_name:
            cog_list = line.split("\t")
            cog_list.pop(0)  # remove first element with the uid
            cog_list.pop(len(cog_list) - 1)  # remove the '/n' at the end of the line
            cog_list[:] = [v for v in cog_list if v != "X"]  # remove all occurrences of "X"
            # insert into the transaction list only new cogs without duplicates
            transaction_list = list(set(transaction_list) | set(cog_list))
        else:
            # reached to a new uid - need to write the transaction into a file
            last_Bacteria_name = curr_Bacteria_name
            if not should_write:  # skip the first that is empty transaction
                should_write = True
            else:
                #transaction_list.sort()
                #label = random.randint(0, 1)
                #transaction_list.append(str(label))
                transaction_list.append("0")  # the label for Humans
                new_line = str(transaction_list).translate({ord('['): '', ord(']'): '', ord('\''): '', ord(" "): ""})
                outputFile.write('%s\n' % new_line)  # save the new transaction into a new line in the file
                cog_list = line.split("\t")
                cog_list.pop(0)  # remove first element with the uid
                cog_list.pop(len(cog_list) - 1)  # remove the '/n' at the end of the line
                cog_list[:] = [v for v in cog_list if v != "X"]  # remove all occurrences of "X"
                # insert into the transaction list only new cogs without duplicates
                transaction_list = cog_list  # replace the old transaction with the new bacteria cogs

    outputFile.close()