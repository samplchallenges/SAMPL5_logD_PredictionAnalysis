import imp
tools = imp.load_source('tools','../../DataFiles/tools.py')
import pickle
from pylab import *

data = pickle.load(open('boxSizeData.p','rb'))

# Get parameters for plot
parameters = tools.JCAMDdict(1)
fig = figure(1)
xlabel('Box Edge (nm)')
ylabel('Solvation Free Energy (kcal/mol)')
ylim(18.25, 19.75)
xlim(2.5,4.75)
ax = fig.add_subplot(111)

# DataFile header
output = ["# Solvation Free Energy by box Size and coloumb interaction type\n", "coloumb type, number of cyclohexanes, box edge (nm), dG, ddG \n"]

# Save handles for legend later:
handles = []

for d, entry in data.items():
    xs = []
    ys = []
    yerr = []
    for num in sorted(entry.keys()):
        edge = entry[num]['size']
        dG = entry[num]['energy'][0]
        ddG = entry[num]['energy'][1]

        xs.append(edge)
        ys.append(dG)
        yerr.append(ddG)

        output.append('%s, %i, %.2f, %.3f, %.3f\n' % (d, num, edge, dG, ddG))

    if d == 'pme':
        sym = 'ro-'
    else:
        sym ='ks-'

    p = ax.errorbar(xs, ys, yerr = yerr, fmt = sym, label = d, capsize = 0.5)
    handles.append(p)

ax.legend(bbox_to_anchor = (0.02, 0.98), loc = 2, ncol = 1, borderaxespad = 0., handles = handles)
savefig('boxSize.pdf')
savefig('../../Paper/boxSize.eps')

f = open('boxSizeData.txt', 'w')
f.writelines(output)
f.close()
