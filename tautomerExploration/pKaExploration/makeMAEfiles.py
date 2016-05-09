import commands as c
import glob
import sys

maeFiles = glob.glob('*mol2')
convertCommand = "/opt/schrodinger/suites2014-4/utilities/structconvert -imol2 %s -omae %s.mae"
allpKaCommand = "/opt/schrodinger/suites2014-4/epik -imae %s.mae -omae %s_allpKa.mae" 

for f in maeFiles:
    samplID = f.split('.')[0]
    print samplID
    # Convert mol2 file to mae file
    print c.getoutput(convertCommand % (f, samplID))
    # Create mae and log file with pKas
    print c.getoutput(allpKaCommand % (samplID, samplID))

