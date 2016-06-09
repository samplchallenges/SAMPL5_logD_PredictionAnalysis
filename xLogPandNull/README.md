# Other Predictions

This directory includes analysis for sets of predictions we imagined people could have submitted, but no one did. 

## Null Hypothesis

One way to evaluate a prediction method is if it performs better than some kind of null hypothesis. 
In the case of distribution coefficients, a good null hypotheiss is that that solute equally prefers water and cyclohexane. This would result in a ratio equal to 1 or a logD = 0.0
Here we assume a prediction set of logD = 0.0 with a model uncertainty of 1.0 log unit and repeat all analysis that was performed all submitted predictions. 

A summary of results is available with the DataFiles

* nullHypothesis.py: Python script that builds the prediction and performs the error analysis using the same procedure followed for all other predictions. 
* NullData.p: A pickled dictionary with all of the error analysis results saved incase we wanted to use them. 

## XLogP predictor

There are many tools available to calcule logP_octanol/water using fast statistical methods based on the structure of the molecule. XlogP in the OpenEye toolkit is an example of such a tool. In this analysis we imagine two possibilities. One where someone directly submitted XlogP predictions as a logD_cyclohexane/water. In the other prediction we use a simple linear fit to fit XlogP predictions to experimental logP_cyclohexane/water values. 

* linearFit.py: This script uses a dictionary from a past project in the Mobley group with experimental data for logP_cyclohexane/water to do a linear fit between the experimental values and the OpenEye XlogP for those compounds. 
* dictionary_logPpaper.p: dictionary needed for the linear fit.
* XLogPAnalysis.py: Uses the OpenEye toolkit's XlogP tool to calculated an estimated logD_cyclohexane for each SAMPL5 molecule. Uses tools module to perform all error analysis on these predictions. 
* XLogP_predictions.p: a pickled dictionary with all data for these predictions, each thing followed by a + indicates the XlogP prediction 'plus' the linear fit. 
* XLogPStats.txt: a text file showing the error analysis for these predictions. 

## Plots
* *_QQ.pdf: A QQ plot created for each of the new predictions
* *_compare.pdf: A comparison plot showing predicted logD versus experimental value for each prediction set
* *_boxPlot: A set of box and whisker plots with prediction and experimental values indicated for each prediction set
