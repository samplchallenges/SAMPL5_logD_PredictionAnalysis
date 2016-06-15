# Written by Caitlin Bannan
# Mobley Group, UC Irvine
# June 2016
# Creates a histogram of the range of experimental logD values
# for the SAMPL5 challenge

import pickle
import tools
from pylab import *

# Get experimental data and make a list
experimental = pickle.load(open('../DataFiles/experimental.p','rb'))
exp = [experimental[k]['data'][0] for k in experimental.keys()] 

# Set up parameters for plot
parameters = tools.JCAMDdict(1)
parameters['figure.subplot.right'] = 0.95
rcParams.update(parameters)

# Make figure
fig = figure(1)
ax = fig.add_subplot(111)

# Add data
print min(exp), max(exp)
bins = [-4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 
        0.5, 1.0, 1.5, 2.0, 2.5] 
ax.hist(exp, bins = bins)

# Add labels and format
ax.set_xlabel(r'binned $\log D$')
ax.set_ylabel(r'count experimental $\log D$')
ax.set_ylim(0,9.5)
ax.set_xlim(-4.5,3.0)
fig.suptitle('Dynamic range experimental distribution coefficients')
savefig('dynamicRange.pdf')
savefig('../Paper/dynamicRange.eps')

