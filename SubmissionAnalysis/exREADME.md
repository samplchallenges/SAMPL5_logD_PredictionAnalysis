# Organizing Experimental data

Main point of this directory is to organize experimental results so they can be used during analysis. 
List of files contained below:

* batch*.txt: These were provided with the SAMPL5 challenge and contain lists of SMPL5 ID numbers in the respective batch
* SMILES_by_ID.txt: Contains SAMPL5 IDs, their SMILES string, and when available their eMolecule ID
* logD_final.txt: was the final list of experimental logD results by SAMPL5_ID


* makeExperimentalDictionary.py: uses above files to create a dictionary with all of the information for each SAMPL5 solute molecule. Generates the output:

All resulting data and pickle files are stored in DataFiles

##### testingDistributions
A directory that should be ignored, it was generated when the Mobley group thought the experimental data would come with uncertainties in the form of confidence intervals

