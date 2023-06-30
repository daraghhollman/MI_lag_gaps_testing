import pandas
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from tqdm import tqdm

matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=["indianred", "mediumturquoise", "palegoldenrod", "cornflowerblue"]) 

def main():
    dataFile = pandas.read_csv("./omni_min_1994.csv")

    parameter = input("What parameter? ")
    
    fig, axes = plt.subplots(3)

    DataGapFrequencyPlot(dataFile[parameter], parameter, axes)
    ViewGapRemoval(dataFile[parameter], parameter, axes)

    fig.subplots_adjust(hspace=0.6)

    plt.show()

def DataGapFrequencyPlot(data, parameter, axes):
    
    ax = axes[0]

    currentGapLength = 0
    gapLengths = []
    for el in tqdm(data):

        if np.isnan(el):
            currentGapLength += 1

        elif currentGapLength > 0:
            gapLengths.append(currentGapLength)
            currentGapLength = 0

    ax.hist(gapLengths, bins=100)
    ax.set_yscale("log")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Gap Length (minutes)")

    ax.margins(0)

    ax.set_title(f"{parameter} gap length")

def ViewGapRemoval(data, parameter, axes):

    if np.max(data) >= abs(np.min(data)):
        data=data[0:int(len(data))]/np.max(data)
    else:
        data=data[0:int(len(data))]/np.min(data)

    ax1 = axes[1]
    ax2 = axes[2]

    time = np.arange(len(data))
    ax1.plot(time, data, color="mediumturquoise")
    ax1.margins(0)
    ax1.set_ylabel("Relative Magnitude (arb.)")
    ax1.set_xlabel("Time (index)")
    ax1.set_title(f"{parameter} with gaps")


    noNanIndices, = np.where(~np.isnan(data))
    dataNoGaps = data[noNanIndices]
    timeNoGaps = np.arange(len(dataNoGaps))

    ax2.plot(timeNoGaps, dataNoGaps, color="cornflowerblue")
    ax2.margins(0)
    ax2.set_ylabel("Relative Magnitude (arb.)")
    ax2.set_xlabel("Time (index)")
    ax2.set_title(f"{parameter} with gaps removed")


if __name__ == "__main__":
    main()
