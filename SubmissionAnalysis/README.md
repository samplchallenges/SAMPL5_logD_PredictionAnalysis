# Analyze SAMPL5 predictions

Main point of this directory is to organize prediction and experimental results
for the SAMPL5 distribution coefficient predictions. 
It includes scripts to organize experimental data and read submission files. 
It also includes scripts for error analysis by prediction and by molecule. 

* Prediction files are in a separate directory and named with their submission number
* SAMPL5_submissionList.txt: This is a complete list of every submission including the name and organization of "non-anonymous" participants and which type of method they used for their calculations. 

* readFiles.py: Collects information from the prediction files and the SAMPL5_users.csv file to make a dictionary of all predictions
* makeExperimentalDictionary.py: uses above files to create a dictionary with all of the information for each SAMPL5 solute molecule. Generates the output:
* AnalyzePredictions.py: This uses the tools module available in DataFiles to perform basic analysis on all sets of predictions. It stores all results from this analysis in DataFiles/predictions.p
* getMoleculeData.py: organizes data by molecule, makes QQPlots, performs error analysis by molecule. Saves all data to a dictionary, pickled and available in DataFiles/
* moleculeStats.py: Collets error metrics by molecule from the dictionary already available. Organizes them into a table, in DataFiles as ErrorMetricsByMolecule.txt and creates the histogram plots by error metric.  
* StatisticsAnalysis.py: Organizes error analysis from prediction dictionary and creates histograms for each error metric



