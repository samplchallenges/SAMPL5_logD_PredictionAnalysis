# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# Provided with topology and coordinate files for a minimized system, return a new coordinate file with precision of 8 decimal places
# This was there would be consistency between the distribution coefficient files and the host-guest files. 

import os
import sys
import commands
import pickle as p

# Dictionary with smile strings keyed at molecule code (SAMPL5_XXX)
database = p.load(open('smiledict.p'))
# Where the minimized files currently are
GenPath = "/work/cluster/bannanc/SAMPL_min/%s/%s/calculation/"
# Where the files should be stored
new_location = "/work/cluster/bannanc/SAMPL_min/SAMPL5_Minimize/" 
current = os.getcwd() #current directory for moving purposes

# Loop through dictionary
for molcode in database.keys():
    # Loop through solvents
    for (solvent,solv_num) in [('water','1000'), ('cyclohexane','500')]:
        # Fill in location of file with solvent and molecule code
        path = GenPath % (solvent, molcode)
        os.chdir(path) # move there
        fileName = "%s-%s" % (solvent, molcode)
        # Use GROMACS commands to get minimized file
        commands.getoutput("echo 0 | gmx trjconv -f minimize2.0.trr -s minimize2.0.tpr -o %s.gro -ndec 8" % fileName)

        # Check that coordinate file was created
        if not os.path.isfile("%s/%s.gro" % (path, fileName)):
            # If it wasn't print a warning
            print molcode, solvent, "gro file not found"
        # Otherwise copy it to your desired location
        else:
            print molcode, solvent
            commands.getoutput("cp %s/%s.gro %s" % (path, fileName, new_location))
        os.chdir(current) # Move back to original location 
         
