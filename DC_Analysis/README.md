# Analyze SAMPL5 predictions

Main point of this directory is to organize prediction results provided by SAMPL5 challenge participants 
and perform general analysis for each prediction set 

##### Input data files

* predictionFiles directory: This directory contains all of the prediction data files provided by participants in the SAMPL5 distribution coefficient challenge.
* SAMPL5_user_mapping.xlsx: excel file with all users contact and other information, provided by D3R team
* SAMPL5_users.csv: converted from the excel file above, with original commas removed to be more easily Python readable. 

* numToSID.p and SIDTonum.p: Dictionaries to convert between random generated submission IDs and assigned 2 digit numbers
* index_table.csv: privides a human readable table of 2 digit numbers and the original file name and submitter name if not anonymous. 

##### Python Scripts

* readFiles.py: Collects information from the prediction files and the SAMPL5_users.csv file to make a dictionary of all predictions
* make_email_list.py: reads emails from SAMPL5_users.csv and makes a text file with all emails in a list
* AnalyzePredictions.py: This uses the tools module available in DataFiles to perform basic analysis on all sets of predictions. It stores all results from this analysis in DataFiles/predictions.p
* getMoleculeData.py: organizes data by molecule, makes QQPlots, performs error analysis by molecule. Saves all data to a dictionary, pickled and available in DataFiles/
* moleculeStats.py: Collets error metrics by molecule from the dictionary already available. Organizes them into a table, in DataFiles as ErrorMetricsByMolecule.txt and creates the histogram plots by error metric.  
* build_index_table.py: Used to make index_table.csv from original version of the dictionary 
* StatisticsAnalysis.py: Organizes error analysis from prediction dictionary and creates histograms for each error metric
* tautomerPlots.py: This script makes comparison plots, but color codes by number of tautomers a molecule has. It also does some brief comparisons to the by molecule analysis
##### Note: Unless updated this directory is not safe for public publishing because it includes contact information and names of Anonymous submissions. 
