# Tautomer Correction

This directory includes all post challenge analysis related to protonation states and tautomer enumeration. 

### Python Scripts

* AnalyzeCorrections.py: This script uses already stored corrections to perform error analysis and create plots for visualizing comparisons. 
* makeMAEfiles.py: Uses Schrodinger tools to perform tautomer enumeration and calculate a state penalty for each SAMPL5 solute 
* ComparingPenalties.py: Reads in data for state penalties calculated by Frank Pickard (NIH) and creates a text file comparing those values with those from Epik
* getStatePenalties.py: This reads the output from Schrodinger ligprep, reads state penalties, stores data in the pKa dictionary and outputs a data table with all possible corrections. 
* unpackTarFiles.py: the ligprep tool creates .maegz files, this script unpacks them so they are easily readable
* getStatePenalties.py: Reads the results files from the ligprep analysis and saves the state penalty corrected logD values to the tautomer dictionary

### Data Files
* ComparingPenalties.txt: Contains state penalties calculated using Schrodinger's Epik tool and those provided by Frank Pickard. 
* penalties_fromPickard.txt: This is the list of state penalties provided by Frank Pickard (NIH). We used them to compare with the Epik state penalties. 
* allLogDs.txt: has the calculated logP corrected to logD by pKa or epik state penalties. 
 
 
