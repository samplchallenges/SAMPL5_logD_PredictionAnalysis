import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pickle
import pylab
import matplotlib.patches as patches

M = pickle.load(open('../moleculeData.p','rb'))

batches = pickle.load(open('../batches.p','rb'))
bat_labels = ['batch0','batch1', 'batch2']

entry = pickle.load(open('XLogP_predictions.p','rb'))

for b, batch in enumerate(batches):
    bat = bat_labels[b]
    print bat
    keys = sorted(batch)
    labels = [k.split('_')[1] for k in keys]
    # preData data is a list of lists of all predicted values for that molecule
    preData = [M[k]['calc'] for k in keys] 

    # expData is a list of floats with the experimental result for that molecule
    e = np.array([M[k]['exp'][0] for k in keys])
    de = np.array([M[k]['dexp'][0] for k in keys])

    # Get My data for this batch:
    my = np.array([entry[k] for k in keys])
    dmy = np.array([0.37 for k in keys])
    # Create figure and axes instances
    fig = plt.figure(1)
    plt.title("Box and Whisker Plot for XLogP %s" % bat)
    ax = fig.add_subplot(111)
    # Create boxplot
    # Folling histogram settings for multiple rows
    # default for whis is 1.5
    bp = ax.boxplot(preData, whis = 100.0)
    ax.set_ylabel('logD')
    ax.set_xticklabels(labels, rotation = 'vertical')
    ax.set_xlabel('SAMPL5_ID#')

    # change line colors
    [fly.set(color = '#7570b3', marker = '.') for fly in bp['fliers']]
    [[box.set(color = '#7570b3') for box in bp[feature]] for feature in ['boxes','caps','medians','whiskers']]

    # Add Experimental Data
    for i in range(len(e)):
        Xs = bp['medians'][i].get_xdata()
        print '\t Xs: ', Xs
        minimum = e[i] - de[i]
        maximum = e[i] + de[i]
        # ax.fill_between(Xs, [maximum, maximum], [minimum, minimum], facecolor = '#ff3377', alpha = 0.9, linewidth = None)
        exp = ax.errorbar(np.average(Xs), e[i], yerr = de[i], fmt = 'ks', label = 'experimental') 
        mine = ax.errorbar(np.average(Xs), my[i], yerr = dmy[i], fmt = 'ro', label = 'XLogP Predictions')
    pred = matplotlib.lines.Line2D([],[], color = '#7570b3', linestyle = 'dashed', label = 'predicted (all)')
    # exp = patches.Patch(color = '#ff3377', label = 'experimental (range)')
    ax.legend(bbox_to_anchor = (1.02, 0.98), loc = 2, ncol = 1, borderaxespad = 0., handles = [pred, exp, mine])
    
    # Save plot and close figure
    fileName = "XLogP_boxPlot_%s.pdf" % ( bat)
    print "making plot ",fileName
    pylab.savefig(fileName, orientation = 'landscape', bbox_inches = 'tight', pad_inches = 0.2)
    plt.close(fig)


