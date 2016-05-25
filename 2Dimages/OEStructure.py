from openeye.oechem import *
from openeye.oegrapheme import *
from openeye.oeiupac import *
import pickle
from openeye.oedepict import *

# Load relavant dictionaries
d= pickle.load(open('../DataFiles/experimental.p','rb'))
molecules = pickle.load(open('../DataFiles/moleculeData.p','rb'))

# Set up figure options
opts = OE2DMolDisplayOptions(200, 200, OEScale_AutoScale)
opts.SetAtomColor(False, OEBlack)
opts.SetTitleLocation(OETitleLocation_Hidden)

for name, e in d.items():
    smile = e['Smiles']
    mol = OEMol()
    OEParseSmiles(mol, smile)
    OEPrepareDepiction(mol, False, True)

    disp = OE2DMolDisplay(mol, opts)
    OERenderMolecule(name+'.pdf',disp)

# Make a LaTeX Table

batches = pickle.load(open('../DataFiles/batches.p','rb'))
batches = [sorted(bat) for bat in batches]

output = ['\\begin{tabular}{c c c}\n', 
        '\\bf{Batch 0} & \\bf{Batch 1} & \\bf{Batch 2} \\\\ \n']

maxlines = max([len(batches[0]), len(batches[1]), len(batches[2])])
print maxlines


for idx in range(maxlines):
    temp = []
    for bat in batches:
        if idx < len(bat):
            temp.append("\\includegraphics[height = 0.05\\textheight]{2DImages/%s.pdf}" % bat[idx])
        else:
            temp.append('')
    output.append("%s & %s & %s \\\\ \n" % (temp[0], temp[1], temp[2]))

# Make Better LaTeX table
output = ['\\begin{tabular}{c c c c c}\n']
image = "\\includegraphics[height = 0.10\\textheight]{2DImages/%s.pdf}"
aue = "%.1f \\pm %.1f" 

ddaue = molecules[name]['AUE']

for idx, bat in enumerate(batches):
    output.append('\\textbf{Batch %i} & & & & \\\\ \n' % idx)
    for line_count in range(len(bat)/5):
        index = line_count*5
        keys = [bat[index+i] for i in range(5)]
        l = [image % k for k in keys]
        output.append("%s & %s & %s & %s & %s \\\\ \n" % (keys[0], keys[1], keys[2], keys[3], keys[4] )
        output.append("%s & %s & %s & %s & %s \\\\ \n" % (l[0], l[1], l[2], l[3], l[4]))
    if idx == 0:
        l = [image % bat[i] for i in range(10,13)]
        output.append("%s & %s & %s & & \\\\ \n" % (l[0], l[1], l[2]))


output.append('\\end{tabular}\n')
f = open("../Paper/MoleculeTable.tex", "w")
f.writelines(output)
f.close()

