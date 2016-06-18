# Mobley logP

The first set of calculations from the Mobley group were partition coefficients (ratio of a single tautomer between cyclohexane and water). These simulations were run and analyzed by Kalistyn H Burley during a rotation project during Fall 2015. 
We used KHB's input files to make example simulation files that were provided for all participants


* AllResults: This directory has results files for all simulations (from Alchemical Analysis)  
* wetCyclohexane_SAMPL5_074: Directory includes all input and results files for the simulation with water in the cyclohexane phase
* allSolvents: input files and trajectory file for simulation with water, cyclohexane, DMSO, and acetonitrile
* boxSize: directory includes all results and input files for the variable boxsize study
* tautomerExploration: has python scripts and results used to extract pKa and state penalty data from Schrodinger tool calculations. 

* XVG_files.tar: archieved directory with GROMACS output files used to calculate the solvation free energy results

* dictionary_AllResults.p is the dictionary created by extractResults.py
* updatedsmiles.p is the empty dictionary with just SAMPL5_IDnumbers and SMILES strings
* DC-MobleySAMPL-1.txt and DCStandard-MobleySAMPL-1.txt: our submission files for SAMPL5
* SAMPL5_withFreeEnergy.txt: Has our logD submission results and the calculated solvation free energies for each molecule. Provided to participants upon request. 
* DC_* distribution coefficient results files as submitted to the SAMPL5 challenge and assigned submission 39
