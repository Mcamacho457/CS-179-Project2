import random
from Location import Location

with open("test_cases/1cluster_test1_2000.txt", "w") as outFile:
    for i in range(0, 2000):
        # generates random x in the range of 0-50
        x = random.randint(0, 50)
        x = float(x)

        # generates random y in the range of 0-50
        y = random.randint(0, 50)
        y = float(y)
        outFile.write(f"   {x}   {y} \n")

with open("test_cases/1cluster_test2_2000.txt", "w") as outFile:
    # this loop generates the data for the 2nd test for when k = 1.
    # we distribute the data as if there are 2 different clusters,
    # but all points should be in one single cluster since k = 1
    for i in range(0, 1000):
        # generates random x in the range of 0-25 (for "1st cluster")
        x = random.randint(0, 25)
        x = float(x)

        # generates random y in the range of 0-25 (for "1st cluster")
        y = random.randint(0, 25)
        y = float(y)
        outFile.write(f"   {x}   {y} \n")
    for i in range(1000, 2000):
        # generates random x in the range of 25-50 (for "2nd cluster")
        x = random.randint(25, 50)
        x = float(x)

        # generates random y in the range of 25-50 (for "2nd cluster")
        y = random.randint(25, 50)
        y = float(y)
        outFile.write(f"   {x}   {y} \n")