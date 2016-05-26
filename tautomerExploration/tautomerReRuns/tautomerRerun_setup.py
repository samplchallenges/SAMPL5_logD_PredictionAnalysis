from solvated_mixtures import *
from MDPandRunMethods import *
import pickle as p
import commands 
import os
import sys # For trouble shooting 

# Location of MDP files (and run.X.sh file)
MDP_path = "MDP_files/"
# Location of pickled dictionary, this can be a path
dictionary = "tautDictionary.p"
# Load dictionary
database = p.load(open(dictionary,'rb'))
# Solvent dictionary
solvents = {'cyclohexane': ['C1CCCCC1',500], 'water': ['O', 1000]}
# Current working directory
current = os.getcwd()

# For both sovents 
for solvent, info in solvents.items():
    smile_solv = info[0]
    num_solv = info[1]
    if not os.path.isdir('./'+solvent):
        os.mkdir('./'+solvent)

    # For every solute 
    for num, entry in database.items():
        # using number for naming because IUPAC names are troublesome
        smile = entry['Smiles']
        solute_dir = "./%s/%s/" % (solvent, num)
        print "Building for %s in %s" % (num, solvent)
        #print "Building for %s (number %s) in %s" % (solute, num, solvent)
        if os.path.isdir(solute_dir):
            continue

        # Use Solvation Toolkit to make solvated boxes
        builder = MixtureSystem([num, solvent], [smile, smile_solv],[1, num_solv], solute_dir)
        builder.run(just_build = True)
        builder.convert_to_gromacs()

        # Move files into calculation folder (you can change this name if you want)
        long_file = "%s_%s_1_%s" % (num, solvent, num_solv)
        calc_dir = "%s/%s/calculation/" % (solvent, num)
        os.mkdir(calc_dir)

        for end in ['gro','top']:
            commands.getoutput("cp %s/gromacs/%s.%s %s/mol.%s" % (solute_dir, long_file, end, calc_dir, end))

        getFiles(MDP_path, calc_dir, jobName = num+'_'+solvent)
        
        # Uncomment this for test runs:
        #sys.exit(1)

        # Uncooment once you know all the set up is working
        # os.chdir(calc_dir)
        # commands.getoutput("for ((n=0; n<20; n++)) do sbatch run.${n}.sh; done")
        os.chdir(current)
