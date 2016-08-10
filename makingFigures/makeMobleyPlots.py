# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# May 2016
# Make plots for Mobley Group simulations and pKa and tautomer corrections

import pickle
from pylab import *
import numpy as np
import imp
tools = imp.load_source('tools','tools.py')

# Load data
experiment = pickle.load(open('../DataFiles/experimental.p','rb'))
data = pickle.load(open('../Mobley_logP/tautomerExploration/dictionary_Corrected.p','rb'))

keys = [k for k in sorted(data.keys())]
# Get experimental data
e = [ experiment[k]['data'][0] for k in keys ]
de = [ experiment[k]['data'][1] for k in keys ]

# get calc data for each set
logP = [data[k]['LogD_calc'][0] for k in keys]
pKa = [data[k]['LogD_oneCorrected'][0] for k in keys]
taut = [data[k]['logD_stateCorrected'][0] for k in keys]

# uncertainty remains the same because we need nothing to estimate the uncertainty in the corrections
dlogD = [data[k]['LogD_calc'][1] for k in keys]

# Get plot parameters
parameters = tools.JCAMDdict(3, True)
wid = parameters['figure.figsize'][0]
parameters['figure.figsize'][1] = wid /2.
parameters['figure.subplot.right'] = 0.97
parameters['figure.subplot.left'] = 0.08
parameters['figure.subplot.bottom'] = 0.15
parameters['figure.subplot.top'] = 0.89
parameters['figure.subplot.wspace'] = 0.2

# parameters['legend.labelspacing'] = 0.1
rcParams.update(parameters)
fig = figure(1)
xLabel = r'Experimental $\log D$'
yLabel = r'Predicted $\log D$'
fig.suptitle("Comparing methods for correcting partition coefficients")

ax1 = tools.ComparePlot([e,e], [pKa, logP], "", xLabel, yLabel, [de,de], [dlogD, dlogD], [r'$\log D_{pK_a}$', r'$\log P$'], limits = [-10, 8], leg = [0.02, 0.98, 2, 1], expError = 1.0, ax1 = fig.add_subplot(121, aspect = 1.0), symbols = ['k^', 'ro' ], white_fill = True)
ax1.set_xlim(-13, 8)
ax1.set_ylim(-13, 8)
ax1.set_xlabel(xLabel)
ax1.set_ylabel(yLabel)

ax2 = tools.ComparePlot([e,e], [taut, pKa], "", xLabel, yLabel, [de,de], [dlogD, dlogD], [r'$\log D_{state\ penalty}$', r'$\log D_{pK_a}$' ], limits = [-10, 8], leg = [0.02, 0.98, 2, 1], expError = 1.0, ax1 = fig.add_subplot(122, aspect = 1.0), symbols = ['bs', 'k^'], white_fill = True)
ax2.set_xlim(-13, 8)
ax2.set_ylim(-13, 8)
ax2.set_xlabel(xLabel)
ax2.set_ylabel(yLabel)



# Save and close fig
savefig('MobleyPlots.pdf')


# =================================================================================
# Add arrows to plot

# Define arrows:
arrow1 = [['050', -3.7, 1.18, -12.5, -8.5],
        ['', -3.73, -9.75, -11.75, -8.5],
        ['060', -4, -3.65, -8, -5 ],
        ['', -4, -7.3, -7.25, -5],
        ['063', -3, -3.7, -4.5, -5.5],
        ['', -3, -6., -3.75, -5.5],
        ['020', 1.7, -3.75, 4, -2]]

arrow2 = [
        ['063', -3, -6., 0, -8.5],
        ['', -3, -9.8, -0.2, -8.5],
        ['060', -4, -7.3, -8, -8.5],
        ['', -4, -8.1, -7.25, -8.5],
        ['050', -3.73, -9.75, -7, -10.5],
        ['', -3.73, -10.75, -6.25, -10.5],
        ['020', 1.7, -3.75, 4, -2]]


# arrow is list of lists with [label, start x, start y, end x, end y]
# switch start and end

# Add arrows to first axis:

for a in arrow1:
    ax1.annotate(a[0], xy = (a[1], a[2]), xytext = (a[3], a[4]), fontsize = 5, arrowprops = dict(arrowstyle ='->', connectionstyle = "arc3,rad = 0.01", linewidth = 0.25))

for a in arrow2:
    ax2.annotate(a[0], xy = (a[1], a[2]), xytext = (a[3], a[4]), fontsize = 5, arrowprops = dict(arrowstyle ='->', connectionstyle = "arc3,rad = 0.01", linewidth = 0.25))

savefig('../Paper/MobleyPlots.eps')
savefig('MobleyPlots_annotated.pdf')
close('all')

# =================================================================================
# Make LaTeX table with my results

output = ['\\begin{tabular}{| l |l |l | l |} \n',
        '\\hline \n',
        'Metric & $\\log P$ & $pK_a$ & state \\\\ \n',
        '\\hline \n']


stats = pickle.load(open('../Mobley_logP/tautomerExploration/CorrectionStats.p', 'rb'))
for met in ['AveErr', 'RMS', 'AUE', 'tau', 'R']:
    logP = stats['LogD_calc'][met]
    pKa = stats['LogD_oneCorrected'][met]
    state = stats['logD_stateCorrected'][met]
    if met == 'AveErr' or met == 'RMS' or met == 'AUE':
        pKa = "$ %.1f \\pm %.1f $" % (pKa[0], pKa[1])
        logP = "$ %.1f \\pm %.1f$" % (logP[0], logP[1])
        state = "$ %.1f \\pm %.1f $" % (state[0], state[1])
    else:
        pKa = "$ %.2f \\pm %.2f $" % (pKa[0], pKa[1])
        state = "$ %.2f \\pm %.2f $" % (state[0], state[1])
        if met == 'R':
            logP = "$ %.1f \\pm %.1f$" % (logP[0], logP[1])
        else:
            logP = "$ %.2f \\pm %.2f$" % (logP[0], logP[1])



    output.append("%s & %s & %s & %s \\\\ \n" % (met, logP, pKa, state))

output.append("\\hline\n")
output.append("\\end{tabular}\n")

f = open("../Paper/MobleyStats.tex", 'w')
f.writelines(output)
f.close()
