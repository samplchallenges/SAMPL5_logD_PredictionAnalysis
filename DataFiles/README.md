# Data Files

This directory contains all data files created during this analysis for easy reference in one place from multiple other directories. 

* experimental.p: dictionary with information about each solute molecule and it's experimentally measured result
* predictions.p: dictionary with information about each set of predictions submitted to SAMPL5, including all error analysis results
* batches.p: list of lists with SAMPL5 molecule IDs by batch with big list as [batch0, batch1, batch2]
* StandardPredictions.p: dictionary with data about predictions done on the Standard examples with provided input files. (Only the Mobley group participated so this data is mostly ignored in future analysis)
* moleculeData.p: dictionary of lists of predictions organized by molecule.  


* emaillist.txt: Just a list of emails separated by commas that makes e-mailing users easier.
* index_table.csv: information about each prediction set in order of assigned (2-digit) ID number


* ErrorMetricsBySubmission_batch*.txt: data table of error metrics for each submission option batch 0; batches 0 and 1; or batches 0, 1 and 2. 
* ErrorMetricByMolecule.txt: data table of error analysis for predictions grouped by molecule
* nullHypothesisData.txt: error analysis results from null hypothesis analysis

* tautomerBatches.txt: We split molecules into new sets based on the number of tautomers they have, this table shows those batches
* tautomerNumbers.txt: A list of SAMPL5_IDnumbers and the number of tautomers it has, maxed set at 100

##### tools.py
A long list of methods that are used in the error analysis for all predictions. 
Included methods for all error metrics, Lipinski's Rule, bootstrapping with or without experimental noise, methods to make the comparison and QQ plots.

##### Note: Unless updated this directory is not safe for public publishing because it includes contact information and names of Anonymous submissions. Prediction Dictionary will need to be updated to remove Names and contact information before being included in public submissions. 
