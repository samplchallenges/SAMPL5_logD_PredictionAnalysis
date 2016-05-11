# Tautomer Correction

This directory includes all post challenge analysis related to protonation states and tautomer enumeration. 

### Python Scripts

* AnalyzeCorrections.py: This script uses already stored corrections to perform error analysis and create plots for visualizing comparisons. The pKa varient is mostly the same, but was built before the state penalties were added and includes some analysis of limited data sets where only the changed logD value was considered. 
* makeMAEfiles.py: Uses Schrodinger tools to perform tautomer enumeration and calculate a state penalty for each SAMPL5 solute 
* ComparingPenalties.py: Reads in data for state penalties calculated by Frank Pickard (NIH) and creates a text file comparing those values with those from Epik
* getStatePenalties.py: This reads the output from Schrodinger ligprep, reads state penalties, stores data in the pKa dictionary and outputs a data table with all possible corrections. 
* unpackTarFiles.py: the ligprep tool creates .maegz files, this script unpacks them so they are easily readable
* getStatePenalties.py: Reads the results files from the ligprep analysis and saves the state penalty corrected logD values to the tautomer dictionary
* PickardCorrections.py: Reads results for state penalties provided by Frank Pickard (NIH) and stores new corrected logD to a dictionary.  
* pKaCorrectedData.py: Loads dictionary of pKas and corrects logP to logD using the calculated pKas and the experimental pH
* LimitedSet_pKa.py: This script performs error analysis looking only at logD values that changed when corrected from logP

### Other files here
* dictionary_allResults.p: This is a dictionary with data from the Mobley group predictions
* dictionary_Corrected.p: This dictionary is continuously added to during this analysis so it has all of the pKas and state penalty corrections included

### DataTables
Text and pdf files with data stored to be human readable

### Plots
Comparison plots and QQ plots for all correction types

### MoleculeFiles
This directory has files for each SAMPL5 molecule used in the analysis including 2D images with pKas labeled. 

### SAMPL5_083

 
 
