import pickle
import numpy as np
import sys
# Openeye used to generate iupac names from smiles
from openeye.oechem import *
from openeye.oeomega import *
from openeye.oeiupac import *

# Files needed
expFile = 'logd_bayes.txt'
startingDictionary = "updatedsmiles.p"

# Get all data from file
f = open(expFile)
data = f.readlines()[1:]
f.close()

# Replace [ and ] with '' and +/- with ','
data = [d.replace(']', '') for d in data]
data = [d.replace('[', '') for d in data]
data = [d.replace('+/-', ',').strip().split(',') for d in data]

# Get keys from first column
keys = [d[0] for d in data]
# Convert the rest of the data to floats
Data = [[float(D) for D in d[1:]] for d in data]
print data[0]
print Data[0], keys[0]

# Load IDs from the first column
# Load dictionary
database_un = pickle.load(open(startingDictionary, 'rb'))
database_low = pickle.load(open(startingDictionary, 'rb'))
database_high = pickle.load(open(startingDictionary, 'rb'))

# Load all batch sets
# batch0 = list(np.genfromtxt('batch0.txt',dtype = str, comments = '#'))
# batch1 = list(np.genfromtxt('batch1.txt',dtype = str, comments = '#'))
# batch2 = list(np.genfromtxt('batch2.txt',dtype = str, comments = '#'))

# Add batch, data, and iupac to dictionary
for i, k in enumerate(keys):
    # add data in the form [logD, dlogD]
    ave = Data[i][0]
    un = Data[i][1]
    lowCI = Data[i][2]
    highCI = Data[i][3]
    # Convert confidence intervals to standard errors
    std_low = (ave - lowCI) / 1.96
    std_high = (highCI - ave) / 1.96
    database_un[k]['data'] = [ave, un]
    database_low[k]['data'] = [ave, std_low]
    database_high[k]['data'] = [ave, std_high]

    #Assign batch
    #if k in batch0:
    #    database[k]['batch'] = 0
    #if k in batch1:
    #    database[k]['batch'] = 1
    #if k in batch2:
    #    database[k]['batch'] = 2
    # Get iupac name from SMILE string
    #print k
    #mol = OEMol()
    #smile = OEParseSmiles(mol, database[k]['Smiles'])
    #if smile:
    #    database[k]['iupac'] = OECreateIUPACName(mol)
    #else:
    #    print k, "missing smile?"

# make dictionary file with everything and batches file with lists of names in batches for future sorting
pickle.dump(database_un,open('experimental_un.p','wb'))
pickle.dump(database_low,open('experimental_low.p','wb'))
pickle.dump(database_high,open('experimental_high.p','wb'))
