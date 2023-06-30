# MI_lag_gaps_testing
A set of tools to view and test the effects data gaps when using arfogg/generic_MI_lag_finder.

## dataGapViewer.py
Creates three panel plots containing:
- A histogram of gap lengths
- A plot of the data including the gaps
- A plot of the data with the gaps removed
<p align="center">
<img src="https://github.com/daraghhollman/MI_lag_gaps_testing/assets/62439417/072fad7f-e73d-400b-b458-d3b3e120662a" width="600"/>
</p>

## runtimeTesting.py
Used to create a plot of relative runtim against the length of the data.
<p align="center">
<img src="https://github.com/daraghhollman/MI_lag_gaps_testing/assets/62439417/a7b50b42-5886-4eae-8f69-38f7b0a562c6" width="600"/>
</p>

## gapsEffect.py
A tool to create plots of the change in the mutual information and lag time based on randomly distributed data gaps increasing the percentage of data missing.

<p align="center">
<img src="https://github.com/daraghhollman/MI_lag_gaps_testing/assets/62439417/69272248-3cb6-4c85-8e82-d9e6107ef9fc" width="600"/>
</p>

## gapsTesting.py
Used to create the data for **gapsEffect.py**
