# Error Analysis Histograms

There is one plot for each batch for each error metric used to analyze the distribution coefficient predictions compared with experiment. 
Uncertainties in these values are calculated using a bootstrapping technique that takes into account the uncertainty in the experimental values. 

* AUE: average unsigned error
* AveErr: average signed error
* maxErr: absolute max deviation from the experimental value
* RMS: root-mean-squared error
* R: Pearson's R
* tau: Kendall's tau
* error slope: slope of the data in the QQ plot, this tells us about how accurate a predictions model uncertainty was. A value over 1 means the model uncertainty is over estimating and a value under 1 corresponds to an underestimated uncertainty.
* compare slope: slope of data in the comparison plot with experimental data on the x-axis. This came out of a discussion at the D3R workshop about how most shown examples of comparison plots had the same shape with a > 1 slope. 
* percent: percent of predictions with the correct sign
* CorrectLipinski: fraction of predictions that correctly guessed rather the logD was within Lipinski's rule, assumes logD in cyclohexane would have the same range as logP in octanol, that is -0.4 to 5.6 log units
 
Predictions were allowed to be submitted for just batch 0, batch 0 and 1, or batch 0, 1, and 2 so analysis is also done for those three options.
Error analysis was repeated for data sets by molecule, where all predictions for that molecule were considered, these files are labeled with _byMolecule. This analysis was used to determine which molecules were difficult for groups to predict.  
