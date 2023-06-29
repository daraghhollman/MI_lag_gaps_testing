import matplotlib.pyplot as plt
import pandas
import numpy as np
from scipy.optimize import curve_fit
from glob import glob

PlotMutualInfo = False
PlotRMS = True


plt.rcParams.update({'font.size': 14})

gapFilesPath = glob("./symh_vs_aeVariableGaps/*.csv")
gapFilesPath.sort()

# print(gapFilesPath)

fileList = []
for filePath in gapFilesPath:
    fileList.append(pandas.read_csv(filePath, dtype=float))

lags = np.arange(-60, 61, 1)
percentages = np.arange(0, 110, 10) # 0 to 100 in batches of 10


mutInfo = []
tPeaks = []
rmsVals =[]

for i, file in enumerate(fileList):
    mutual_information = file["mutual_information"][0:-1]

    if "x_piecewise_df.t_peak" in file:
        tPeak = file["x_piecewise_df.t_peak"][0]
        tPeaks.append(tPeak)

    if "x_piecewise_df.RMS" in file:
        RMS = file["x_piecewise_df.RMS"][0]
        rmsVals.append(RMS)

    mutInfo.append(mutual_information)
    print(np.max(mutual_information))


mutInfo = np.transpose(mutInfo)

if PlotMutualInfo:
    plt.pcolormesh(percentages, lags, mutInfo, shading="flat", cmap="viridis")
    plt.colorbar(label="Mutual Information (nats)")

    centrePos = [pos+5 for pos in percentages[0:-1]]
    plt.scatter(centrePos, tPeaks, color="black", label="x_piecewise_df.t_peak", marker="x")

    def LinearFunc(x, m, c):
        return m*x + c

    linPars, linCov = curve_fit(LinearFunc, centrePos, tPeaks)

    fittingPercentages = np.linspace(0, 100, 1000)
    plt.plot(fittingPercentages, LinearFunc(fittingPercentages, linPars[0], linPars[1]), linewidth=2, linestyle="dashed", color="red", label=f"Linear Fit ($y=mx+c$)\n$\quad$m = {linPars[0]:.5f}\n$\quad$c = {linPars[1]:.5f}")

    # Offset ticks to represent the first bin being 0%
    plt.xticks(ticks=np.arange(10, 10*len(percentages), 10), labels=percentages[0:-1])
    plt.grid(axis="x", color="black")

    plt.xlabel("Percentage of data missing")
    plt.ylabel("Lag Time (minutes)")

    plt.title("SYMH against AE with varying amounts missing data")
    plt.legend()

    plt.show()

if PlotRMS:
    plt.scatter(percentages[0:-1], rmsVals, marker="x", color="black", label="RMS")

    def QuadFunc(x, a, b, c):
        return a*x**2 + b*x + c

    def ExpFunc(x, a, b, c, d):
        return a*np.exp(b*x+c)+d

    expPars, expCov = curve_fit(ExpFunc, percentages[0:-1], rmsVals, [1, 1, -90, 1])

    fittingPercentages = np.linspace(0, 100, 1000)
    plt.plot(fittingPercentages, ExpFunc(fittingPercentages, expPars[0], expPars[1], expPars[2], expPars[3]), color="indianred", label="Exponential Fit")

    plt.ylabel("RMS")
    plt.xlabel("Percentage of data missing")
    plt.margins(0)

    plt.legend()

    plt.show()
