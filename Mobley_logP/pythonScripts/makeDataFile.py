# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# January/February 2016 I don't remember
# Prints calculated logD and associated solvation free energies to text file. It is the same script I used to make our SAMPL5 submission, solvation free energies were add later when discussing results with other participants

import pickle as p

a = p.load(open('dictionary_allResults.p','rb'))
tF = open('SAMPL5_withFreeEnergy.txt','w')
rms = 1.4 
print >> tF, "# SAMPL ID, logD, stat unc., model unc., dF wat, ddF wat, dF cyc, ddF cyc"
dataKeys = sorted([k for k in a.keys()])

for num in dataKeys:
    logD = a[num]['LogD_calc'][0]
    dlogD = a[num]['LogD_calc'][1]
    wat = a[num]['water']
    cyc = a[num]['cyclohexane']
    data = "%s, %.2f, %.2f, 1.4, %.1f, %.1f, %.1f, %.1f" % (num, logD, dlogD, -wat[0], wat[1], -cyc[0], cyc[1])
    print data
    print >>tF, data

tF.close()
