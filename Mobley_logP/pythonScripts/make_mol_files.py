#!/bin/env python

#Import stuff we need
from openeye.oechem import * #Basic OEChem toolkits
from openeye.oeomega import * #Conformation generation
from openeye.oeiupac import * #Chemical naming
import pickle as p
import sys

dictionary = "dictionary.p"
database = p.load(open(dictionary,'rb'))

omega = OEOmega() #Initialize class
omega.SetMaxConfs(1) #Only generate one conformer for each

# These setting will present issues if the smile strings are not stereo specific, but I don't see it being a problem here 
omega.SetStrictStereo(True)  
omega.SetStrictAtomTypes(True)

#Actually loop over database contents
for molname, entry in database.items():
    num = entry['number']
    smile = entry['smile']
    print num, molname
    #Create new OEChem mol to hold molecule
    mol = OEMol()
    #Try and parse SMILE
    status = OEParseSmiles(mol, smile)
    #Generate conformation, store if successful
    if status:
        #Gen conf
        canMake = omega(mol)

        if canMake:
            #Update molecule title
            mol.SetTitle(molname)
            #Write to .mol2 file
            ofile = oemolostream(num+'.mol2')
            OEWriteMolecule(ofile, mol)
            ofile.close()
            # Write to .sdf file
            ofile = oemolostream(num+'.sdf')
            OEWriteMolecule(ofile, mol)
            ofile.close()
    else:
        print "was not parseable"
    print
    # Uncomment this for test runs
    # sys.exit(1)
