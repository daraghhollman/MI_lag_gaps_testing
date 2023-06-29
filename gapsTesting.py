import generic_mutual_information_routines as genMI
import pandas
import numpy as np
from tqdm import tqdm
import random


def main():
    # to test the gaps we use a data field without gaps and sample the gaps from another file. Here we use AE and flow pressure

    data1994 = pandas.read_csv("./omni_min_1994.csv")
    
    ae = data1994["ae"]
    symh = data1994["symh"]

    # Find and record the positions of the gaps
    aeGaps = GapDataRandomly(ae, 0.1)

    # Next we can compare aeGaps against ae to check if the correlation changes.
    print("Running mi_lag_finder... maybe make a cup of tea :) ")
    lags, mutInfo, RPS_mutual_information, x_squared_df, x_piecewise_df, minEntropy = RunMILag(symh, aeGaps)

    SaveOutput(lags, mutInfo, x_piecewise_df, "./symh_vs_aeVariableGaps/symh-ae_10gaps.csv")



def RunMILag(stationaryArray, laggedArray):
    ax, lags, mutual_information, RPS_mutual_information, x_squared_df, x_piecewise_df, minEntropy = genMI.mi_lag_finder(np.array(stationaryArray), np.array(laggedArray), remove_nan_rows=True, check_entropy=True)

    return (lags, mutual_information, RPS_mutual_information, x_squared_df, x_piecewise_df, minEntropy)    


def GapDataRandomly(fieldWithGaps, gapAmount):
    # Function to randomly 
    
    newFieldWithGaps = []
    for el in fieldWithGaps:
        if random.random() < gapAmount:
            newFieldWithGaps.append(np.nan)
        else:
            newFieldWithGaps.append(el)

    # print(newFieldWithGaps)

    return newFieldWithGaps


def GapDataFromData(fieldWithoutGaps, fieldWithGaps):
    # Function to recreate data gaps in a datafield without them using the gaps from the field with gaps as a template
    
    print("Finding gap locations...")
    newFieldWithGaps = []
    numGaps = 0
    for fullVal, gapsVal in tqdm(zip(fieldWithoutGaps, fieldWithGaps), total=len(fieldWithoutGaps)):
        if np.isnan(gapsVal):
            newFieldWithGaps.append(gapsVal)
            numGaps += 1
        else:
            newFieldWithGaps.append(fullVal)

    print(f"New data created with percentage gaps: {numGaps * 100 / len(fieldWithoutGaps)}%")
    return newFieldWithGaps


def SaveOutput(lags, mutual_information, x_piecewise_df, path):
    print("Saving output...")
    data = {
        "lags": lags,
        "mutual_information": mutual_information,
    }
    
    dfOutput = pandas.DataFrame(data)
    dfOutput.insert(2, "x_piecewise_df.t_peak", x_piecewise_df.t_peak)
    dfOutput.insert(3, "x_piecewise_df.RMS", x_piecewise_df.RMS)

    dfOutput.to_csv(path)



if __name__ == "__main__":
    main()
