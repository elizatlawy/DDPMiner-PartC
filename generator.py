import random
import string
from random import randrange

# file = open("generated_data2.csv", "w")
#file = open("generated_1000_cogs_per_trans.csv", "w")

letter_array = [c for c in string.ascii_lowercase]
num_list = list(range(0, 10))


def generate():
    for i in range(1, 10000):
        random.shuffle(letter_array)
        pattern = letter_array[:random.randint(8, 12)]
        label = random.randint(0, 1)
        pattern.append(str(label))
        file.write(",".join(pattern) + "\n")


def generate_cogs():
    for k in range(1,100):
        for i in range(1, 1000):
            cog = ""
            for j in range(0, 4):
                cog = cog + str(randrange(10))
            file.write(cog + ",")
        label = random.randint(0, 1)
        file.write(str(label) + "\n")
