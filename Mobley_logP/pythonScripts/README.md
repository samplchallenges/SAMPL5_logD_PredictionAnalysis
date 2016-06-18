# Mobley logP

The first set of calculations from the Mobley group were partition coefficients (ratio of a single tautomer between cyclohexane and water). These simulations were run and analyzed by Kalistyn H Burley during a rotation project during Fall 2015. 
We used KHB's input files to make example simulation files that were provided for all participants

* makeDataFile.py: gets data from the results dictionary and prints it to a text file. 
* extractResults.py: extracts results from the Alchemical Analysis output data structures
* getAlchemicalResults.py: extracts free energy results from GROMACS xvg output using Alchemical Analysis
* DC_* distribution coefficient results files as submitted to the SAMPL5 challenge and assigned submission 39
* getmin8.py: Used GROMACS conversion tools to output coordinate files with 8 decimal places
* fixcombo.py: used fixXVG to combine original xvg files with xvg files created by the simulation restart
* fixXVG.py: A modulated script with methods that removes corrupt lines from xvg files and a method to combine multiple xvg files from the same trajectory that were separated by GROMACS restarts
* dipolemoment.py: Calculates the dipolemoment for each molecule based on charges in the mol2 file.  
