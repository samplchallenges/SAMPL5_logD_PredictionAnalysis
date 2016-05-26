# Molecule Files 

This directory has files for each SAMPL5 molecule that were used in pKa and tautomer enumeration calculations. Types are listed below, where * indicates any SAMPL5_IDnumber

* *.mol2: Molecule file provided for the SAMPL5 challenge
* *.sdf: Molecule file provided for the SAMPL5 challenge
* *.mae: Created by calling Schrodinger's "utilities/structconvert -imol2 *.mol2 -omae *.mae" 
* *_allpKa*: Output files created with Schrodinger's Epik tool by calling "epik -imae *.mae -omae *_allpKa.mae"
* *_pKa.png: A 2D image of the molecule with individual pKas labeled
* ligprep*.*: Files created with Schrodinger's Ligprep tool by calling "ligprep -imae *.mae -omae ligprep_*.maegz -bff 14 -pH 7.4 -retain_i -ac -s 32 -r 1 -epik" and then calling "utilities/structconvert -imae ligprep_*.maegz -omae ligprep_*.mae"

There is also an extra file for ligprep_SAMPL5_083_conformer2 which is actually the second tautomer. That ligprep analysis was performed mannually in Maestro with the SMILES string for the second tautomer. 
