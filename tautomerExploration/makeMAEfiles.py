# Written by Caitlin C Bannan
# Mobley Group, University of California Irvine
# February 2016
# This script uses the schrodinger tool ligprep to analyze all the SAMPL5 molecule files and perform a tautomer enumeration to get a state penalty for the tautomer used in our analysis

import commands as c
import os
import glob
import sys

#convertCommand = "/opt/schrodinger/suites2014-4/utilities/structconvert -imol2 %s -omae %s.mae"
#allpKaCommand = "/opt/schrodinger/suites2014-4/epik -imae %s.mae -omae %s_allpKa.mae" 

LigPrepCommand = "/opt/schrodinger/suites2014-4/ligprep -imae %s.mae -omae ligprep_%s.maegz -bff 14 -ph 7.4 -retain_i -ac -s 32 -r 1 -epik"
maeFiles = glob.glob('../MoleculeFiles/SAMPL5_*.mae')
for f in maeFiles:
    samplID = f.split('.')[0]
    if os.path.isfile('ligprep_%s.maegz' % samplID):
        continue
    print samplID
    # Create mae and log file with pKas
    print c.getoutput(LigPrepCommand % (samplID, samplID))


