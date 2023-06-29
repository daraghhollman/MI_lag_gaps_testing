import generic_mutual_information_routines as genMI
import pandas
from tqdm import tqdm
import time
import numpy as np
import matplotlib.pyplot as plt

def main():
    data1994 = pandas.read_csv("./omni_min_1994.csv")
    data1995 = pandas.read_csv("./omni_min_1995.csv")

    ae94 = data1994["ae"]
    ae95 = data1995["ae"]

    totalData = pandas.concat([ae94, ae95])

    oneWeek = totalData[0:10080] # 10080 minutes in one week
    oneMonth = totalData[0:43800]
    threeMonth = totalData[0:131400]
    sixMonth = totalData[0:262800]
    twelveMonth = totalData[0:525600]
    eighteenMonth = totalData[0:788400]
    twentyFourMonth = totalData

    times = [10080, 43800, 262800, 525600, 788400, 1052000]
    datalist = [oneWeek, oneMonth, threeMonth, sixMonth, twelveMonth, eighteenMonth, twentyFourMonth]

    calculateTimes = True
    plotData = True

    if calculateTimes == True:
        # Run MI Lag for each time-length
        runtimes = []
        for data in tqdm(datalist, total=len(datalist)):
            startTime = time.time()
            RunMILag(data, data)
            endTime = time.time()

            timeTaken = endTime - startTime
            runtimes.append(timeTaken)

        np.savetxt(r"./runtimes.txt", [times, runtimes])

    if plotData == True:
        data = np.loadtxt(r"./runtimes.txt")
        times = data[0]
        runtimes = [el/data[1][0] for el in data[1]]

        plt.scatter(times, runtimes, color="cornflowerblue")
        plt.ylabel("Relative Run Time")
        plt.xlabel("Data Length (minutes)")

        plt.show()


def RunMILag(stationaryArray, laggedArray):
    ax, lags, mutual_information, RPS_mutual_information, x_squared_df, x_piecewise_df = genMI.mi_lag_finder(np.array(stationaryArray), np.array(laggedArray))

    return (lags, mutual_information, RPS_mutual_information, x_squared_df, x_piecewise_df)    


if __name__ == "__main__":
    main()
