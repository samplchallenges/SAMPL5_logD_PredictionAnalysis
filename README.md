# Distribution Coefficients Analysis of Predictions

Prediction analysis of distribution coefficient part of the SAMPL5 challenge. 

Caitlin C Bannan

David L Mobley

### Sub Directories:
This is a short description, detailed READMEs included inside each.

##### DataFiles
Contains all pickled data files so they can be easily accessed in one place. 
Also includes all text data tables and the tools modules so they can be easily accessed. 

##### organizeExpData
Contains scripts and text files required to generate dictionary with experimental results, SMILES string, eMolecule ID, IUPAC name, and batch number for each solute molecule

##### DC_Analysis 
Contains scripts and text files used to create a dictionary with all data from predictions submitted to SAMPL5

##### QQPlots, ComparePlots, and boxPlots
Each plot type has one for each prediction set (and batch in the case of box and whisker plots). 

##### statsPlots
A histogram for each error metric and each batch showing how each prediction set did. These are sorted from best to worst by that metric. 

##### 2Dimages
Contains a 2D image of each solute molecule. 

##### Distribution Coefficient Analysis
This seems to be a repeat of things in the top folder - CCB: I'm not sure why it's here, but I didn't delete it 

##### otherPredictions
This directory includes all information for analysis of theoretical prediction sets including if someone were to submit a "null hypothesis" or logD = 0.0 for everything or if they had used a logP predictor with little to no correction for cyclohexane instead of octanol. 

##### BestGroups
An analysis was done taking the average of the 6 best "groups" in the top 10 predictions by average unsigned error. This directory has the resulting plots and data related to this combined analysis

##### Paper
Tex document and figures required for our paper to be submitted in June 2016. 

### return_results.py
Used to e-mail participants with data specifically related to their performance in the challenge. 

##### Note: Unless updated this directory is not safe for public publishing because it includes contact information and names of Anonymous submissions.
