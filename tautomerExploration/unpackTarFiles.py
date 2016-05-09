# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# Un-archieves maegz files using Schrodinger tools  

import commands as c
import os
import glob
import sys

#convertCommand = "/opt/schrodinger/suites2014-4/utilities/structconvert -imol2 %s -omae %s.mae"
#allpKaCommand = "/opt/schrodinger/suites2014-4/epik -imae %s.mae -omae %s_allpKa.mae" 

unpackCommand = "/opt/schrodinger/suites2014-4/utilities/structconvert -imae %s -omae %s.mae"

LigPrepCommand = "/opt/schrodinger/suites2014-4/ligprep -imae %s.mae -omae ligprep_%s.maegz -bff 14 -ph 7.4 -retain_i -ac -s 32 -r 1 -epik"
maeFiles = glob.glob('*.maegz')
for f in maeFiles:
    # samplID = "SAMPL5_"+f.split('.')[0].split('_')[-1]
    # if os.path.isfile('ligprep_%s_epik.log' % samplID):
        # continue
    base = f.split('.')[0]
    print base
    # Create mae and log file with pKas
    print c.getoutput(unpackCommand % (f, base))
    # print c.getoutput('tar -xvf %s' % f)


