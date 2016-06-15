# Distribution Coefficients Analysis of Predictions

Prediction analysis of distribution coefficient part of the SAMPL5 challenge. 

* Caitlin C Bannan
* Kalistyn H Burley
* Michael Chui
* Michael K Gilson
* David L Mobley

##### Note: Unless updated this directory is not safe for public publishing because it includes contact information and names of Anonymous submissions.
I am triple checking this now, we should be able to make it public by the time we submit the paper

##### DataFiles
Contains all pickled data files so they can be easily accessed in one place. 
Also includes all text data tables and the tools modules so they can be easily accessed. 

##### PredictionFiles_byNumber
These are the prediction submissions provided by participants. 
They have been renamed with the assigned submission number to make them easier to locate.

##### SubmissionAnalysis 
Contains scripts used to create a dictionary with all experimental data and predictions submitted to SAMPL5
Contains scripts and text files required to generate dictionary with experimental results, SMILES string, eMolecule ID, IUPAC name, and batch number for each solute molecule
Includes all error analysis and scripts to make plots for all submissions

##### QQPlots, ComparePlots, and boxPlots
Each plot type has one for each prediction set (and batch in the case of box and whisker plots). 

##### statsPlots
A histogram for each error metric and each batch showing how each prediction set did. These are sorted from best to worst by that metric. 

##### 2Dimages
Contains a 2D image of each solute molecule. 

##### Distribution Coefficient Analysis
This seems to be a repeat of things in the top folder - CCB: I'm not sure why it's here, but I didn't delete it 

##### xLogPandNull
This directory includes all information for analysis of theoretical prediction sets including if someone were to submit a "null hypothesis" or logD = 0.0 for everything or if they had used a logP predictor with little to no correction for cyclohexane instead of octanol. 

##### BestGroups
An analysis was done taking the average of the 6 best "groups" in the top 10 predictions by average unsigned error. This directory has the resulting plots and data related to this combined analysis

##### Mobley_logP
This directory contains the analysis for our reference calculations. 
It includes a number of subdirectories for this analysis:
* tautomerExploration: This directory involves calculations to correct Mobley group predictions of logP to logD using a variety of techniques to enumerate protonation states in water. (With one attempt to enumerate tautomers in cyclohexane)
* AllResults: Contains the results output from Alchemical Analysis, both the text and pickle file
* boxSize: Contains the input and results files and complete analysis for the brief study checking that box size does not affect the calculated solvation free energy. 


##### MoleculeFiles
This directory has files for each SAMPL5 molecule, including input files for our reference calculations and all relevant Schrodinger Epik and LigPrep files

##### Making Figures
This directory includes most scripts used to make figures and tables used in the published paper


