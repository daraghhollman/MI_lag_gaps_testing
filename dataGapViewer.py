import pandas
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

def main():
    dataFile = pandas.read_csv("./omni_min_1994.csv")

    parameter = input("What parameter? ")
    
    DataGapFrequencyPlot(dataFile[parameter])

def DataGapFrequencyPlot(data):
    
    currentGapLength = 0
    gapLengths = []
    for el in tqdm(data):

        if np.isnan(el):
            currentGapLength += 1

        elif currentGapLength > 0:
            gapLengths.append(currentGapLength)
            currentGapLength = 0

    plt.hist(gapLengths)
    plt.yscale("log")
    plt.ylabel("Frequency")
    plt.xlabel("Gap Length (minutes)")

    plt.show()

if __name__ == "__main__":
    main()
