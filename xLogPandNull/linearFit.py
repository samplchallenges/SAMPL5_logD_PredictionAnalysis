# Written by Caitlin C Bannan
# Mobley Group, University of California Irvine
# February 2016
"""
This script uses data from one of our past projects to do a linear fit from xlogP predictions for logP_octanol/water to an experimental logP_cyclohexane/water. 

The linear fit is used in other analysis to see how a corrected xLogP would have done for a logDcyc/wat calculation.
"""

import pickle
from sigfig.sigfig import *
import sys
import glob
import numpy as np
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')
from openeye.oechem import *
from openeye.oemolprop import *
from openeye.oeiupac import *

# Load old dictionary
data = pickle.load(open('dictionary_Leo1971paper.p','rb'))
# Using only one prediction so I'm calling it e to match the old code:
e = {}
for cid, entry in data.items():
    num = entry['number']
    print num
    smile = entry['smile']
    # Generate OEMol
    mol = OEMol()
    OEParseSmiles(mol, smile)
    #Get logP
    e[num] = {}
    e[num]['XLogP'] = OEGetXLogP(mol)
    e[num]['LogPcyc'] = entry['cyclohexane']['LogP_exp'][0]

# Organize by batch
nums = [entry['number'] for (cid, entry) in data.items()]
allExp = [e[num]['LogPcyc'] for num in nums]
dallExp = [0.3 for num in nums]

calc = [ e[num]['XLogP'] for num in nums]
dcalc = [0.37 for num in nums]

# Use tools to plot data  
title = "OpenEye's XLogP compared to Leo Hansch LogPcyc"
# Using larger of the two uncertainties for this plot
tools.ComparePlot(allExp, calc, title, "Experimental logD", "Predicted logD", dallExp, dcalc, [''], "logPpaper_XLogP_compare.pdf")

# Make the linear fit:
y = np.array(calc)
x = np.array(allExp)
m, b = np.linalg.lstsq(np.vstack( [x, np.ones(len(allExp))]).T, y)[0]
print "Linear fit of x=experiment and y = XlogP gives slope = %.4f and intercept = %.4f" % (m,b)
b_dif = np.average(y-x)
print "If we set the slope = 1, the average intercept = %.4f" % b_dif

