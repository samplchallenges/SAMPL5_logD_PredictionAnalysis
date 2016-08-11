# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# May 2016
# Make plots for Mobley Group simulations and pKa and tautomer corrections

import pickle
import imp
import sys
tools = imp.load_source('tools','../DataFiles/tools.py')

null = pickle.load(open('../xLogPandNull/NullData.p'))
xlogp = pickle.load(open('../xLogPandNull/XLogP_predictions.p'))
# =================================================================================
# Make LaTeX table with my results

output = ['\\begin{tabular}{| l |l |l | l |} \n',
        '\\hline \n',
        'Metric & Null  & $XlogP_{oct}$ & $XlogP_{corr}$ \\\\ \n',
        '\\hline \n']


for met in ['AveErr', 'RMS', 'AUE', 'tau', 'R']:
    n = null[met]
    x = xlogp[met]
    c = xlogp[met+'+']
    if met == 'AveErr' or met == 'RMS' or met == 'AUE':
        n = "$ %.1f \\pm %.1f $" % (n[0], n[1])
        x = "$ %.1f \\pm %.1f $" % (x[0], x[1])
        c = "$ %.1f \\pm %.1f $" % (c[0], c[1])

    else:
        x = "$ %.2f \\pm %.2f $" % (x[0], x[1])
        c = "$ %.2f \\pm %.2f $" % (c[0], c[1])
        if met == 'R' or met == 'tau':
            n = 'N/A'
        else:
            n = "$ %.2f \\pm %.2f $" % (n[0], n[1])

    output.append("%s & %s & %s & %s \\\\ \n" % (met, n, x, c))

output.append("\\hline\n")
output.append("\\end{tabular}\n")

f = open("../Paper/otherPredictions.tex", 'w')
f.writelines(output)
f.close()
