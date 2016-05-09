from openeye.oechem import *
from openeye.oeiupac import *
import pickle
from openeye.oedepict import *

d= pickle.load(open('../experimental.p','rb'))

for name, e in d.items():
    smile = e['Smiles']
    mol = OEMol()
    OEParseSmiles(mol, smile)
    mol.SetTitle(name)
    OEPrepareDepiction(mol)
    OERenderMolecule(name+'.pdf',mol)


