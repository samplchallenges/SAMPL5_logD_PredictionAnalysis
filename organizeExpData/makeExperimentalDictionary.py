# Written by Caitlin C Bannan
# Mobley lab, University of California Irvine
# January 2016
"""
This script creates a dictionary of all experimental results for the distribution coefficient part of SAMPL5. 
It reads in data from a number of text files and saves the information to a pickled dictionary. 
Experimental data provided by Arien Sebastiaan (Bas) Rustenburg from the Chodera Lab at MSKCC
"""

import pickle
import numpy as np
# Openeye used to generate iupac names from smiles
from openeye.oechem import *
from openeye.oeiupac import *
from openeye.oequacpac import *

# Extract lines from SMILES file provided by SAMPL5 challenge
smilesFile = 'SMILES_by_ID.txt'
f = open(smilesFile)
smilelines = f.readlines()
smilelines = smilelines[1:] # Remove header line
f.close()

# Add lines to dictionary keyed by SAMPL5 ID
database = {}
for line in smilelines:
    items = line.split(',')
    key = items[0].strip() # SAMPL5 ID
    smile = items[1].strip() # SMILES string
    emolecule = items[2].strip() # eMolecules ID, '' if not available

    # Add key to dictionary
    database[key] = {'Smiles': smile, 'eMolecule': emolecule}

# Experimendal data
expFile = 'logD_final.txt'

# Load data as [exp, unc] for each item
Data = np.genfromtxt(expFile, skip_header = 3, delimiter = ',',usecols = (1,2))
# Load IDs from the first column
keys = np.genfromtxt(expFile, dtype = str,skip_header = 3, delimiter = ',',usecols = (0))
# Load all batch sets
batch0 = list(np.genfromtxt('batch0.txt',dtype = str, comments = '#'))
batch1 = list(np.genfromtxt('batch1.txt',dtype = str, comments = '#'))
batch2 = list(np.genfromtxt('batch2.txt',dtype = str, comments = '#'))

# Add batch, data, and iupac to dictionary
for i, k in enumerate(keys):
    # add data in the form [logD, dlogD]
    database[k]['data'] = Data[i]
    #Assign batch
    if k in batch0:
        database[k]['batch'] = 0
    if k in batch1:
        database[k]['batch'] = 1
    if k in batch2:
        database[k]['batch'] = 2

    # Get calculated information about the molecule
    mol = OEGraphMol()
    smile = OEParseSmiles(mol, database[k]['Smiles'])
    if smile:
        # Add iupac name to dictionary
        database[k]['iupac'] = OECreateIUPACName(mol)
        
        # Set tautomer enumeration settings
        tautomerOptions = OETautomerOptions(100, True) # Max enumerated is 100
        tautomerOptions.SetCarbonHybridization(True)
        tautomerOptions.SetMaxZoneSize(50)
        tautomerOptions.SetApplyWarts(True)
        tautomerOptions.SetSaveStereo(True)
        
        # Save number of tautomers 
        database[k]['tautomers'] = len([t for t in OEEnumerateTautomers(mol, tautomerOptions) ] )
    else:
        print k, "missing smile?"

# make dictionary file with everything and batches file with lists of names in batches for future sorting
pickle.dump(database,open('../DataFiles/experimental.p','wb'))
pickle.dump([batch0,batch1,batch2], open('../DataFiles/batches.p','wb'))
