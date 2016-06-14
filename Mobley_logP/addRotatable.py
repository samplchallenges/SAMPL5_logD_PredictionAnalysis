import pickle
from operator import itemgetter, attrgetter
from openeye.oechem import *
from openeye.oemolprop import *
from openeye.oezap import *
from openeye.oeiupac import *
import numpy as np

database = pickle.load(open('dictionary_allResults.p','rb'))

for (name, entry) in database.items():
    mol = OEMol()
    OEParseSmiles(mol, entry['Smiles'])
    database[name]['rotatable'] = OECount(mol, OEIsRotor())
    
pickle.dump(database, open('dictionary_allResults.p','wb'))

molecules = pickle.load(open('../DataFiles/moleculeData.p','rb'))

keys = [n for n in database.keys()]
rots = [database[n]['rotatable'] for n in keys]
aue = [molecules[n]['AUE'][0] for n in keys]
combo = zip(keys, rots, aue)
combo = sorted(combo, key = itemgetter(2))

for k, r, a in combo:
    print "%s,\t %i, \t %.3f" % (k, r, a)

batches = pickle.load(open('../DataFiles/batches.p','rb'))

rots = [ [database[n]['rotatable'] for n in bat ] for bat in batches]

print 'batch 0', np.average(rots[0])
print 'batch 1', np.average(rots[1])
print 'batch 2', np.average(rots[2])

all_rots = rots[0] + rots[1] + rots[2]
 
print 'everything', np.average(all_rots)
