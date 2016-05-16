# Tautomer Correction

This directory includes all post challenge analysis related to protonation states and tautomer enumeration. 

### Python Scripts
Below is the list of all python scripts in analysis order

* makeMAEfiles.py: Uses Schrodinger tools to perform tautomer enumeration and calculate a state penalty for each SAMPL5 solute, lines also included for Epik pKa calculations. 
* unpackTarFiles.py: the ligprep tool creates .maegz files, this script unpacks them so they are easily readable
* pKaCorrections.py: reads log files from Epik pKa calculations, saving pKa data to dictionary and then calculates new logDs from each pKa correction option. 
* getStatePenalties.py: This reads the output from Schrodinger ligprep, reads state penalties, stores data in the pKa dictionary and outputs a data table with all possible corrections. 
* addPickardCorrections.py: Reads data file provided by Frank Pickard (NIH) and stores data to dictionary, creates a few data files as well
* LimitedSet_pKa.py: This script performs error analysis looking only at logD values that changed when corrected from logP
* AnalyzeCorrections.py: This script uses already stored corrections to perform error analysis and create plots for visualizing comparisons. It includes a variety of plot options 


* dictionary_allResults.p: This is a dictionary with data from the Mobley group predictions
* dictionary_Corrected.p: This dictionary is continuously added to during this analysis so it has all of the pKas and state penalty corrections included

* ArtsResults.xlsx: This is an excel spreadsheet provided by Art Bochevarov at Schrodinger. He used their Jaguar tool to enumerate tautomers for SAMPL5_050 in cyclohexane and water. Caitlin added the last sheet which shows how the tautomer analysis affects the predicted logD. (Art and David are likely writing up this analysis separately so it will probably not be included in the SAMPL5 prediction analysis paper)

### DataTables
Text and pdf files with data stored to be human readable

### Plots
Comparison plots and QQ plots for all correction types

### SAMPL5_083
This molecule was a particularly tricky one, it is a large macrocycle with many different tautomers and protonation states. With the help of Andreas Klamt, we performed analysis on a few different tautomers of this molecule
 
 
