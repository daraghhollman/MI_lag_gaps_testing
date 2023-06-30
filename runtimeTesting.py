import generic_mutual_information_routines as genMI
import pandas
from tqdm import tqdm
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit

def main():
    matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=["indianred", "aquamarine", "palegoldenrod", "cornflowerblue"]) 
    matplotlib.rcParams.update({'font.size': 18})

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

    times = [10080, 43800, 131400, 262800, 525600, 788400, 1052000]
    datalist = [oneWeek, oneMonth, threeMonth, sixMonth, twelveMonth, eighteenMonth, twentyFourMonth]

    calculateTimes = False
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

        print(runtimes)
        np.savetxt(r"./runtimes.txt", [times, runtimes])

    if plotData == True:
        data = np.loadtxt(r"./runtimes.txt")
        times = data[0]
        runtimes = [el/data[1][0] for el in data[1]]

        linPars, cov = curve_fit(LinearFunc, times, runtimes)
        quadPars, cov = curve_fit(QuadraticFunc, times, runtimes)

        xRange = np.arange(0, np.max(times), 10)

        plt.plot(times, runtimes, label="Runtimes", linestyle="None", marker="o", zorder=10)

        plt.plot(xRange, LinearFunc(xRange, linPars[0], linPars[1]), label="Linear Fit")
        plt.plot(xRange, QuadraticFunc(xRange, quadPars[0], quadPars[1], quadPars[2]), label="Quadratic Fit")

        plt.ylabel("Relative Run Time")
        plt.xlabel("Data Length")

        plt.xticks(np.delete(times, 1), ["1 Week", "3 Months", "6 Months", "1 Year", "1.5 Years", "2 Years"])

        plt.legend()

        plt.show()


def LinearFunc(x, m, c):
    return m*x + c

def QuadraticFunc(x, a, b, c):
    return a*x**2 + b*x + c


def RunMILag(stationaryArray, laggedArray):
    ax, lags, mutual_information, RPS_mutual_information, x_squared_df, x_piecewise_df = genMI.mi_lag_finder(np.array(stationaryArray), np.array(laggedArray))

    return (lags, mutual_information, RPS_mutual_information, x_squared_df, x_piecewise_df)    


if __name__ == "__main__":
    main()
