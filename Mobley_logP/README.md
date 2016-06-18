# Mobley logP

The first set of calculations from the Mobley group were partition coefficients (ratio of a single tautomer between cyclohexane and water). These simulations were run and analyzed by Kalistyn H Burley during a rotation project during Fall 2015. 
We used KHB's input files to make example simulation files that were provided for all participants

 

* getmin8.py: uses commands module and GROMACS commands to retreive a minimized solvated both and create a coordinate file with 8 decimal precision - this script was used on green planet where the input files were stored, the top and gro files are in the Simulation files so they are not provided separately here.  
* makeDataFile.py: gets data from the results dictionary and prints it to a text file. 
* AllResults: This directory has results files for all simulations (from Alchemical Analysis)  
* Method.* were draft files for writing the method that was incldued in our submission file (39)
* DC-MobleySAMPL-1.txt and DCStandard-MobleySAMPL-1.txt: our submission files for SAMPL5
* SAMPL5_withFreeEnergy.txt: Has our logD submission results and the calculated solvation free energies for each molecule. Provided to participants upon request. 
* wetCyclohexane_SAMPL5_074: Directory includes all input and results files for the simulation with water in the cyclohexane phase
* allSolvents: input files and trajectory file for simulation with water, cyclohexane, DMSO, and acetonitrile
