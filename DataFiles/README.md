# Data Files

This directory contains all data files created during this analysis for easy reference.
The scripts to create them are in a number of other directories. 

* experimental.p: dictionary with information about each solute molecule and it's experimentally measured result
* predictions.p: dictionary with information about each set of predictions submitted to SAMPL5, including all error analysis results
* batches.p: list of lists with SAMPL5 molecule IDs by batch with big list as [batch0, batch1, batch2]
* moleculeData.p: dictionary of lists of predictions organized by molecule.  


* SMILES_by_SAMPL5_ID.txt: has SAMPL5_IDnumbers and corresponding SMILES string
* experimental.txt: the experimental logD values and uncertainties
* batch*.txt: This is a list by SAMPL5_ID of molecules in that batch
* ErrorMetricsBySubmission_batch*.txt: data table of error metrics for each submission option batch 0; batches 0 and 1; or batches 0, 1 and 2. 
* ErrorMetricByMolecule.txt: data table of error analysis for predictions grouped by molecule
* nullHypothesisData.txt: error analysis results from null hypothesis analysis


##### tools.py
A long list of methods that are used in the error analysis for all predictions. 
Included methods for all error metrics, Lipinski's Rule, bootstrapping with or without experimental noise, methods to make the comparison and QQ plots.

