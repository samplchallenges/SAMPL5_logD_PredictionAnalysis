# Written by Caitlin C Bannan
# Mobley Group, UC Irvine
# Makes Table 1 for SAMPL5 DC paper
# It has error metrics for every submission

import pickle

# Load submission data
predictions = pickle.load(open('../DataFiles/predictions.p','rb'))

# Set up first few lines in table
output = ["\\footnotesize\n", "\\begin{tabular}{l r r r r r r}\n", "\\hline\n"]
# Add table headers
output.append("ID & Ave. err. & RMS & AUE & tau & R & Err. slope \\\\ \n")
output.append("\\hline\n")

# We will need to get data for groups that didn't submit every batch so first we will add data to the lines.
only0 = [4, 13, 24, 37, 52, 59, 67, 69]
only1 = [1, 3, 50, 55, 70]
Metrics = ['AveErr','RMS','AUE','tau','R', 'maxErr', 'error slope']



for k in sorted(predictions.keys()):
    e = predictions[k] # wrote with items, but then realized I wanted it sorted
    # Get batch
    if k in only0:
        bat = "batch0"
    elif k in only1:
        bat = "batch1"
    else: # Included all batches
        bat = "batch2"
    
    # Collect statistics and format into strings
    Ave = "$%.1f \\pm %.1f$" % (e[bat]['AveErr'][0],e[bat]['AveErr'][1]) 
    RMS = "$%.1f \\pm %.1f$" % (e[bat]['RMS'][0],e[bat]['RMS'][1]) 
    AUE = "$%.1f \\pm %.1f$" % (e[bat]['AUE'][0],e[bat]['AUE'][1]) 
    tau = "$%.2f \\pm %.2f$" % (e[bat]['tau'][0],e[bat]['tau'][1]) 
    R = "$%.2f \\pm %.2f$" % (e[bat]['R'][0],e[bat]['R'][1]) 
    slope = "$%.2f \\pm %.2f$" % (e[bat]['error slope'][0],e[bat]['error slope'][1]) 

    # Add data as line in output (with superscript when applicable)
    if k in only0:
        output.append("%02d\\textsuperscript{a} & %s & %s & %s & %s & %s & %s \\\\ \n" % (k, Ave, RMS, AUE, tau, R, slope)) 
    elif k in only1:
        output.append("%02d\\textsuperscript{b} & %s & %s & %s & %s & %s & %s \\\\ \n" % (k, Ave, RMS, AUE, tau, R, slope)) 
    else:
        output.append("%02d & %s & %s & %s & %s & %s & %s \\\\ \n" % (k, Ave, RMS, AUE, tau, R, slope)) 

# Add end of tabular information
output.append("\\hline \n")
output.append("\\end{tabular}\n")
# output.append("\\textsuperscript{a} submission included only molecules in batch 0. \\textsuperscript{b} submission included only molecules in batches 0 and 1. \n")

f = open("../Paper/groupStats.tex", "w")
f.writelines(output)
f.close()
