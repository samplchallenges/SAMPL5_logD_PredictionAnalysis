# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# May 2016
# Making example figures for the SAMPL5_DC paper, the supporting info with have all of the extra figures. 

import pickle
from pylab import *
import numpy as np
import imp
tools = imp.load_source('tools','../DataFiles/tools.py')

# Load data
predictions = pickle.load(open('../DataFiles/predictions.p','rb'))
batches = pickle.load(open('../DataFiles/batches.p','rb'))
experiment = pickle.load(open('../DataFiles/experimental.p','rb'))

# Get experimental data
e = [ [ experiment[k]['data'][0] for k in batch ] for batch in batches ]
de = [ [ experiment[k]['data'][1] for k in batch ] for batch in batches ]

# ==========================================================================================
# Example comparison and QQ plots
parameters = tools.JCAMDdict(3, True)
parameters['figure.subplot.right'] = 0.95
parameters['figure.subplot.left'] = 0.10
parameters['figure.subplot.bottom'] = 0.1
parameters['figure.subplot.top'] = 0.95
parameters['figure.subplot.hspace'] = 0.35
parameters['figure.subplot.wspace'] = 0.35
# parameters['legend.labelspacing'] = 0.1
rcParams.update(parameters)
fig = figure(1)
xLabel = r'Experimental $\log D$'
yLabel = r'Predicted $\log D$'
# Get 23's data and make comparison plot
c23 = [ [ predictions[23]['data'][k][0] for k in batch ] for batch in batches ]
dc23 = [ [ predictions[23]['data'][k][1] for k in batch ] for batch in batches ]
ax1 = tools.ComparePlot(e, c23, "Compare to experiment for submission 23", xLabel, yLabel, de, dc23, ['batch 0', 'batch 1', 'batch 2'], limits = [-13, 12], leg = [0.02, 0.98, 2, 1], expError = 1.0, ax1 = fig.add_subplot(221))
ax1.set_xlim(-13, 12)
ax1.set_ylim(-13, 12)
ax1.set_xlabel(xLabel)
ax1.set_ylabel(yLabel)
ax1.set_title('Compare submission 23 to experiment')

# Get 49's data and make comparison plot
c49 = [ [ predictions[49]['data'][k][0] for k in batch ] for batch in batches ]
dc49 = [ [ predictions[49]['data'][k][1] for k in batch ] for batch in batches ]
ax2 = tools.ComparePlot(e, c49, "Compare to experiment for submission 49", xLabel, yLabel, de, dc49, ['batch 0', 'batch 1', 'batch 2'], limits = [-15.5, 8.0], leg = [0.02, 0.98, 2, 1], expError = 1.0, ax1 = fig.add_subplot(222))
ax2.set_xlim(-15.5, 8.0)
ax2.set_ylim(-15.5, 8.0)
ax2.set_xlabel(xLabel)
ax2.set_ylabel(yLabel)
ax2.set_title('Compare submission 49 to experiment')

# Get 23's QQ data and make QQ plot
QQdata = predictions[23]['batch2']['QQdata']
slope = predictions[23]['batch2']['error slope'][0]
ax3 = tools.makeQQplot(QQdata[0], QQdata[1], slope, 'Q-Q plot for submission 23', ax1 = fig.add_subplot(223), leg = [0.02, 0.98, 2, 1]) 
ax3.set_xlabel("Expected fraction within range")
ax3.set_ylabel("Fraction of predictions within range")
ax3.set_title('Submission 23 Q-Q plot')

# Get 49's QQ data and make QQ plot
QQdata = predictions[49]['batch2']['QQdata']
slope = predictions[49]['batch2']['error slope'][0]
ax4 = tools.makeQQplot(QQdata[0], QQdata[1], slope, 'Q-Q plot for submission 49', ax1 = fig.add_subplot(224), leg = [0.02, 0.98, 2, 1]) 
ax4.set_xlabel("Expected fraction within range")
ax4.set_ylabel("Fraction of predictions within range")
ax4.set_title('Submission 49 Q-Q plot')

savefig('../Paper/ExamplePlots.eps')
savefig('ExamplePlots.pdf')
close('all')


# ==========================================================================================
# Make "Best in group comparison figure
# ==========================================================================================
# Adjust figure height
width = parameters['figure.figsize'][0]
parameters['figure.figsize'][1] = width / 3.0
parameters['figure.subplot.right'] = 0.9
parameters['figure.subplot.left'] = 0.08
parameters['figure.subplot.bottom'] = 0.2
parameters['figure.subplot.top'] = 0.90
parameters['legend.labelspacing'] = 0.1
parameters['figure.subplot.wspace'] = 0.3
rcParams.update(parameters)

# Create figure and subplots
fig = figure(1)
axes = [fig.add_subplot(131), fig.add_subplot(132), fig.add_subplot(133)]

# Add data for all plots
for idx, num in enumerate([16, 36, 14]):
    # get calculated data
    c = [ [ predictions[num]['data'][k][0] for k in batch ] for batch in batches ]
    dc = [ [ predictions[num]['data'][k][1] for k in batch ] for batch in batches ]

    # use tools to make comparison plot
    if idx == 2:
        leg = [0.82, 1.0, 2, 1]
    else:
        leg = None
    ax1 = tools.ComparePlot(e, c, "Compare to experiment for submission %i" % num, xLabel, yLabel, de, dc, ['batch 0', 'batch 1', 'batch 2'], limits = [-13, 12], leg = leg, expError = 1.0, ax1 = axes[idx])
    ax1.set_xlim(-12, 8)
    ax1.set_ylim(-12, 8)
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel, labelpad = 0.35)
    ax1.set_title("Submission %i" % num)

# Save and close figure
savefig('../Paper/BestGroups.eps')
savefig('BestGroups.pdf')
close('all')

# ==========================================================================================
# Make histogram figures
# ==========================================================================================

# Adjust parameters, these figures will be three histograms across, where each histogram takes two rows
paramters = tools.JCAMDdict(w = 3, fontsize = 6) 
width = parameters['figure.figsize'][0]
parameters['figure.figsize'][1] = width * (np.sqrt(5.0) - 1.0) / 2.4 
parameters['figure.subplot.right'] = 0.975
parameters['figure.subplot.left'] = 0.06
parameters['figure.subplot.top'] = 0.90
parameters['figure.subplot.hspace'] = 0.2
parameters['figure.subplot.wspace'] = 0.25
rcParams.update(parameters)

# Load lists of data for first figure
mets1 = ['RMS', 'AveErr', 'AUE']
mets2 = ['tau', 'R', 'error slope']

# Other factors by figure
files = [ ['ErrorMetrics.pdf', '../Paper/ErrorMetrics.eps'], ['CorrelationMetrics.pdf', '../Paper/CorrelationMetrics.eps'] ]
options = [ [None, None, None], ['reverse', 'reverse', 'close to 1'] ] 
absolutes = [True, False]

# Get keys and submission IDs
keys = [k for k in predictions.keys() if predictions[k].has_key('batch2')]
subIDs = ["%02d" % k for k in keys]

for idx, metrics in enumerate([mets1, mets2]):
    # create figure and assign parameters
    fig = figure(1, frameon = False)
    fig.suptitle("Error Metrics by Submission ID")
    axes_list = [ [fig.add_subplot(231), fig.add_subplot(234)], [fig.add_subplot(232), fig.add_subplot(235)], [fig.add_subplot(233), fig.add_subplot(236)] ]     

    # Make histogram for each batch
    for index, met in enumerate(metrics):
        # Load values
        vals = [predictions[k]['batch2'][met][0] for k in keys]
        dvals = [predictions[k]['batch2'][met][1] for k in keys]
        
        # Make plots
        axes_list[index] = tools.histPlot(subIDs, vals, dvals, "Submission Number", met, '', option = options[idx][index], absolute = absolutes[idx], ax = axes_list[index])
        axes_list[index][0].set_ylabel(met, labelpad = 0.35, fontsize = 6)
        axes_list[index][1].set_ylabel(met, labelpad = 0.35, fontsize = 6)
    # Save and close figure
    fig.set_frameon(False)
    savefig(files[idx][0])
    savefig(files[idx][1])
    close('all')

