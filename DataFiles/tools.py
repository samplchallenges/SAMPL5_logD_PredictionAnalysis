# =============================================================================
# Adapted from David Mobley's script for PharmSci 272
#   and scripts process_submissions.py and uncertainty_check.py from SAMPL4
# By Caitlin C. Bannan
# February 2016
# =============================================================================

import numpy
from numpy import *
import scipy
import scipy.stats
import matplotlib. pyplot as plt
import matplotlib.patches as patches
from pylab import *
import scipy.integrate
from operator import itemgetter, attrgetter

def rmserr( set1, set2 ):
    """Compute and return RMS error for two sets of equal length involving the same set of samples."""
    tot = 0.
    for i in range(len(set1)):
        tot+= (set1[i] - set2[i])**2
    return sqrt(tot/float(len(set1)))

def correl(x,y ):
    """For two data sets x and y of equal length, calculate and return r, the product moment correlation. """
    xar = numpy.array(x)
    yar = numpy.array(y)


    #Compute averages (try not to require numerical library)
    avgx=sum(xar)/float(len(xar))
    avgy=sum(yar)/float(len(yar))

    #Compute standard deviations
    sigmax_sq=0
    for elem in xar:
        sigmax_sq+=(elem-avgx)**2
    sigmax_sq=sigmax_sq/float(len(xar))
    sigmay_sq=0
    for elem in yar:
        sigmay_sq+=(elem-avgy)**2
    sigmay_sq=sigmay_sq/float(len(yar))

    sigmax=sqrt(sigmax_sq)
    sigmay=sqrt(sigmay_sq)

    #Compute numerator of r
    num=0
    for i in range(len(xar)):
        num+=(xar[i]-avgx)*(yar[i]-avgy)
    #Compute denominator of r
    denom=len(xar)*sigmax*sigmay

    corr = num/denom
    return corr

def percent_within_half( x, y, compare = 0.5):
    """
    input: x and y should be equal length arrays
    compare is a float the difference will be compared to

    returns: percent of values within the 'compare' value
    """

    diff = x - y
    indices = where( abs(diff) < compare)
    return 100.*float(len(indices[0]) )/float(len(x))    

def RemoveNones(data, remove=None):
    """
    Given a numpy array of arrays this will remove columns in the array where the value for any row is 'remove'

    input: data = numpy array  of any length with any number of rows
        remove = the value that if found in any row that entire column will be removed
    """
    shape = len(data.shape)
    if shape == 1:
        test  = array([data]) 
    else:
        test = data.copy()
    
    delRows = []
    for i in range(len(test[0])): 
        if None in list(test[:,i]):
            delRows.append(i)

    test = delete(test, delRows, 1)
    if shape == 1:
        return test[0]
    else:
        return test

def CorrectSign(x, y):
    """
    input: two arrays (or lists) of the same length
    output: percent of the values that agree with sign
    """
    xar = numpy.array(x)
    yar = numpy.array(y)
    agree = float(numpy.sum(numpy.sign(xar) == numpy.sign(yar)))
    return agree/float(len(x)) * 100.0

def MeanSignDeviation(x,y):
    """
    Calculates the mean signed deviation (mean sign error)
    that is MSD = sum(y_i - x_i) / n
    """
    x = array(x)
    y = array(y)
    sumDif = sum(y-x)
    
    return sumDif / len(x)
    
# Copied from David L. Mobley's scripts written for SAMPL4 analysis (added calculation uncertainty)
def bootstrap( datasets ):
    """Take a list of datasets of equal length. Use bootstrap to construct a new list of datasets of the same length and return them. The procedure is to select random data point indices (running from 0 to the set length, with replacement) and construct new datasets from those indices from each of the specified sets."""

    #Initialize storage; determine length of set
    newsets = []
    npoints = len( datasets[0] )
    
    #Pick random datapoint indices
    idx = numpy.random.randint( 0, npoints, npoints) #Create an array consisting of npoints indices, where each index runs from 0 up to npoints. 

    for dataset in datasets:
        newsets.append( dataset[idx] )
        #Error check
        if len(dataset) <> npoints:
            raise BaseException("Error: Variable length datasets passed to bootstrap function, which is not acceptable. Terminating.")

    return newsets 

# Copied from David L. Mobley's scripts written for SAMPL4 analysis (added calculation uncertainty)
def bootstrap_exptnoise( calc1, expt1, exptunc1, returnunc = False):
    """Take two datasets (equal length) of calculated and experimental values. Construct new datasets of equal length by picking, with replacement, a set of indices to use from both sets. Return the two new datasets. To take into account experimental uncertainties, random noise is added to the experimental set, distributed according to gaussians with variance taken from the experimental uncertainties. Approach suggested by J. Chodera.

Optionally, 'returnunc = True', which returns a third value -- experimental uncertainties corresponding to the data points actually used."""
    
    # Make everything an array just in case
    calc = array(calc1)
    expt = array(expt1)
    exptunc = array(exptunc1)
    npoints = len(calc)

    #Pick random datapoint indices
    idx = numpy.random.randint( 0, npoints, npoints) #Create an array consisting of npoints indices, where each index runs from 0 up to npoints.

    #Construct initial new datasets
    newcalc = calc[idx]
    newexpt = expt[idx]
    newuncExp = exptunc[idx]

    #Add noise to experimental set
    noise = numpy.random.normal( 0., exptunc) #For each data point, draw a random number from a normal distribution centered at 0, with standard devaitions given by exptunc
    newexpt += noise

    if not returnunc:
        return newcalc, newexpt
    else:
        return newcalc, newexpt, newuncExp

# Copied from David L. Mobley's scripts written for SAMPL4 analysis (added calculation uncertainty)
# CCB: I want to add an optional bootstrap with or without noise, I think this can be done without defining a separate function
def stats_array( calc1, expt1, exptunc1, boot_its, sid = "Number?", noise = True):
    """Compute statistics given sets of calculated and experimental values, experimental uncertainties, and a number of bootstrap iterations, for error estimates.

    Returns: 
        avgerr/d_avgerr: Average error and error estimate
        RMS/d_RMS: RMS error and error estimate
        AUE/d_AUE: AUE and error estimate
        tau/d_tau: Kendall tau and error estimate REMOVED
        R, d_R: Pearson R and error estimate
        maxE, d_maxE: Maximum error and uncertainty
        per, d_per: percent calculated with correct sign
        """
    # Assign array type to gaurentee calculations will work correctly
    # Allows users to submit anything "list like" 
    calc = np.array(calc1, dtype = np.float64)
    expt = np.array(expt1, dtype = np.float64)
    exptunc = np.array(exptunc1, dtype = np.float64)

    #COMPUTE OVERALL PERFORMANCE
    #Compute various metrics -- average error, average unsigned error, RMS error, Kendall Tau, Pearson correlation coefficient and Percent Correct Sign
    per = CorrectSign(calc, expt) 
    #Avg err
    avgerr = (calc - expt).mean()
    #RMS err
    RMS = numpy.sqrt( 1./float(len(expt)) * ((expt-calc)**2).sum() )
    #Average unsigned error
    AUE = numpy.abs( calc - expt).mean()
    #Tau
    tau, ptau = scipy.stats.kendalltau( expt, calc)
    #Pearson R
    R, pr = scipy.stats.pearsonr( expt, calc )
    #Max
    maxE = max(abs(calc-expt))
    r2 = correl(expt, calc) 
    #DO BOOTSTRAP ERROR ANALYSIS FOR OVERALL PERFORMANCE
    print "   Bootstrap for %s..." % sid
    avgerrs = numpy.zeros( boot_its)
    RMSerrs = numpy.zeros( boot_its)
    AUEs = numpy.zeros(boot_its)
    taus = numpy.zeros(boot_its)
    Rs = numpy.zeros(boot_its)
    maxEs = numpy.zeros(boot_its)
    pers = numpy.zeros(boot_its)
    r2s = numpy.zeros(boot_its)
    for it in range(boot_its):
        if noise:
            [ c, e ] = bootstrap_exptnoise( calc, expt, exptunc)  #Generate new sets, adding appropriate random variation to the experimental set.
        else:
            [ c, e ] = bootstrap( [calc, expt] ) # Generate new sets without adding noise to the experimental set
        avgerrs[it] = (c-e).mean()
        RMSerrs[it] =  numpy.sqrt( 1./float(len(e)) * ((e-c)**2).sum() )
        AUEs[it] = numpy.abs( c - e).mean()
        taus[it], p = scipy.stats.kendalltau( e, c)
        Rs[it], p = scipy.stats.pearsonr( e, c)
        maxEs[it] = max(abs( e-c))
        pers[it] = CorrectSign(c, e)
        r2s[it] = correl(e, c)

    return [avgerr, avgerrs.std()], [RMS, RMSerrs.std()], [AUE, AUEs.std()],[tau, taus.std()], [R, Rs.std()], [maxE, maxEs.std()], [per, pers.std()], [r2, r2s.std()] 
     

# Metho for making plots comparing calculated and experimental Data
def ComparePlot(x, y, Title, XLabel, YLabel, xerr, yerr, labels, fileName = 'compare.pdf', limits = None, leg = [1.02, 0.98, 2, 1],expError = 1.0, wOption = 1):
    """ Input:
        x, y, xerr, yerr = list of arrays to be plotted 
        Title, XLabel, YLabel = strings for labeling plot
        labels = list of labels for the legend
        fileName = string, optional, save plot to file
        limits = list with [lowlimit, highlimit] default used if None
        leg = list of legend settings, in order, both bbox_to_anchor placement, location number, and number of columns 
        expError = shaded region of plot
    """
    rcParams.update(JCAMDdict(wOption))

    symbols = ['ro','bs','gD','rx','bo','gs']
    # If limits not provided find the low and high
    if limits == None:
        # adjustment so limits are aleast as big as error bars 
        maxXerr = np.max([i for k in xerr for i in k])
        maxYerr = np.max([i for k in yerr for i in k])
        adjust = np.max([maxXerr, maxYerr]) + 0.5
        # Find limits find the minimum and maximum of all data
        allvals = [i for k in x for i in k]
        allvals += [i for k in y for i in k]
        lowLim = min(allvals) - adjust
        highLim = max(allvals) + adjust
    # Otherwise use the ones provided
    else:
        lowLim = limits[0]
        highLim = limits[1]

    # Set up so that multiple sets of data can be passed, so if only one set is passed make it a list of lists still
    try:
        len(x[0])
    except:
        x = [x]
        y = [y]
        xerr = [xerr]
        yerr = [yerr]
        
    # Initial Plot settings
    fig1 = plt.figure(1)
    ylim(lowLim, highLim)
    xlim(lowLim, highLim)
    plt.xlabel(XLabel)
    plt.ylabel(YLabel)
    plt.title(Title)
    ax1 = fig1.add_subplot(111)
    handles = []

    # Add data to plot for each set
    for i in range(len(x)):
        p1 = ax1.errorbar(x[i],y[i], xerr = xerr[i], yerr = yerr[i], fmt = symbols[i], label = labels[i], capsize = 0.5)
        handles.append(p1)

    # Insert range for "correct" prediction
    L = numpy.array([lowLim-20, highLim +20])
    ax1.plot(L,L, 'k-', markersize = 6.0)
    ax1.fill_between(L, L+expError, L-expError, facecolor = 'wheat', alpha = 0.5, label = "Agree within %.1f" % expError)
    yellow = patches.Patch(color = 'wheat', label = r'$\pm$ %0.1f log units' % expError)
    handles.append(yellow)

    # Add legend
    ax1.legend(bbox_to_anchor = (1.02, 0.98), loc = 2, ncol = 1, borderaxespad = 0., handles = handles)

    savefig(fileName)

    plt.close(fig1)

# ===============================================================================
# Methods from uncertain_check.py David L. Mobley wrote for the SAMPL4 analysis
# ===============================================================================

def normal( y):
    """Return unit normal distribution value at specified location."""
    return 1./sqrt(2*pi) * exp( -y**2/2. )

def compute_range_table( stepsize = 0.001, maxextent = 10  ):
    """Compute integrals of the unit normal distribution and return these tabulated. Returns:
- range: NumPy array giving integration range (x) where integration range runs -x to +x
- integral: NumPy arrange giving integrals over specified integration range.

Arguments (optional):
- stepsize: Step size to advance integration range by each trial. Default: 0.001
- maxextent: Maximum extent of integration range
"""
    #Calculate integration range
    x = arange( 0, maxextent, stepsize )  #Symmetric, so no need to do negative values.
    
    #Calculate distribution at specified x values
    distrib = normal(x)

    integral = zeros( len(x), float)
    for idx in range(1, len(x)):
        integral[idx] = 2*scipy.integrate.trapz( distrib[0:idx+1], x[0:idx+1] ) #Factor of 2 handles symmetry

    return x, integral 

def get_range( integral, rangetable, integraltable):
    """Use rangetable and integral table provided (i.e. from compute_range_table) to find the smallest range of integration for which the integral is greater than the specified value (integral). Return this range as a float."""

    idx = where( integraltable > integral)[0]
    return rangetable[ idx[0]]


#[DLM]Precompute integral of normal distribution so I can look up integration range which gives desired integral
#integral_range, integral = compute_range_table()



def fracfound_vs_error( calc, expt, dcalc, dexpt, integral_range, integral):
    """
    Takes in calculated and experimental values, their uncertainties as well as 
    """
    #Fraction of Gaussian distribution we want to compute
    X = arange( 0, 1.0, 0.01) 
    Y = zeros( len(X))

    for (i, x) in enumerate(X):
        #Determine integration range which gives us this much probability
        rng = get_range( x, integral_range, integral)
        #print x, rng       
 
        #Loop over samples and compute fraction of measurements found
        y = 0.
        #for n in range(0, len(DGcalc)):
        #    sigma_eff = sqrt( sigma_calc[n]**2 + sigma_expt[n]**2 )
        #    absdiff = abs( DGcalc[n] - DGexpt[n])
        #    #print absdiff, n, sigma_eff
        #    if absdiff < rng * sigma_eff: #If the difference falls within the specified range of sigma values, then this is within the range we're looking at; track it
        #        #print "Incrementing y for n=%s, x = %.2f" % (n, x)
        #        y += 1./len(DGcalc)
        #Rewrite for speed
        sigma_eff = sqrt( array(dcalc)**2 + array(dexpt)**2)
        absdiff = sqrt( (array(calc) - array(expt))**2)
        idx = where( absdiff < rng*sigma_eff)[0] 
        Y[i] = len(idx) * 1./len(calc)

    #print Y
    #raw_input()

    return X, Y

# ===============================================================================
# Use methods above to make QQ-plot and return "error slope"
# ===============================================================================

def getQQdata(calc, expt, dcalc, dexpt, boot_its):
    """
    Takes calculated and experimental values and their uncertainties 
    """
    integral_range, integral = compute_range_table()
    X, Y = fracfound_vs_error(calc, expt, dcalc, dexpt, integral_range, integral)
    xtemp = X[:,numpy.newaxis]
    coeff,_,_,_ = numpy.linalg.lstsq(xtemp, Y)
    slope = coeff[0]
    slopes = []
    for it in range(boot_its):
        n_calc, n_expt, n_dexpt = bootstrap_exptnoise(calc, expt, dexpt, returnunc = True)
        nX, nY = fracfound_vs_error(n_calc, n_expt, dcalc, n_dexpt, integral_range, integral)
        a, _, _, _ = numpy.linalg.lstsq(xtemp, nY)
        slopes.append(a[0])
    return X, Y, slope, numpy.array(slopes).std()

def makeQQplot(X, Y, slope, title, xLabel ="Expected fraction within range" , yLabel ="Fraction of predictions within range", fileName = "QQplot.pdf", uncLabel = 'Model Unc.', leg = [1.02, 0.98, 2, 1] ):
    """
    Provided with experimental and calculated values (and their associated uncertainties) in the form of list like objects. 

    Provides the analysis to make a QQ-plot using the guassian integral methods David wrote for SAMPL4 that are included above.

    Makes a files of the plot and returns the "error slope" as a float and the figure of the created plot
    """
    # Get plot parameters for JCAMD
    rcParams.update(JCAMDdict())

    # Set up plot
    fig1 = plt.figure(1)
    ylim = (0,1)
    xlim = (0,1)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    ax1 = fig1.add_subplot(111)

    # Add data to plot
    p1 = ax1.plot(X,Y,'bo', label = uncLabel)

    # Add x=y line
    p2 = ax1.plot(X,X,'k-', label = r'$X=Y$')

    # X data needs to be a column vector to use linalg.lstsq
    p3 = ax1.plot(X, slope*X, 'r-', label = 'Slope %.2f' % slope)

    # Build Legend 
    handles = [p1,p2,p3]
    ax1.legend(bbox_to_anchor = (leg[0], leg[1]), loc = leg[2], ncol = leg[3], borderaxespad = 0.)

    # Adjust spacing then save and close figure
    savefig(fileName) 
    plt.close(fig1)

def histPlot(subIDs, vals, dvals, xLabel, yLabel, title, option = None, fileName = None, absolute = True, widOption = 4):
    """"
    Makes histogram plots of data at IDs with sorted data. Provide settings for plot, including labels and titles. Saved out to fileName. 
    option is the way the data should be sorted, if None it is from smallest to largest vals the other options are reverse (or from largest to smallest vals) or 'close to 1' which sorts based on which value is closest to one.
    """
    # Get plot parameters for JCAMD
    parameters = JCAMDdict(widOption, True)
    parameters['figure.subplot.right'] = 0.9
    rcParams.update(parameters)

    if absolute: # want to compare absolute vlues 
        temp = zip(subIDs, abs(array(vals)), dvals)
    else: # No absolute value:
        temp = zip(subIDs, array(vals), dvals)

    # Use sorting option to sort data
    if option == None: # Normal Sort
        temp = sorted(temp, key = itemgetter(1))
    elif option.lower() == 'reverse': # Sort biggest to smallest
        temp = sorted(temp, key = itemgetter(1), reverse = True)
    elif option.lower() == 'close to 1': # Sort by value closest to 1
        def close_to_one(x, y):
            if abs(1-x) < abs(1-y): return -1
            else: return 1
        temp = sorted(temp, key = itemgetter(1), cmp = close_to_one)
    # else Don't sort 

    # "unzip" values and undo absolute value if it was used
    (sids, tempVals, metricuncs) = zip(*temp)
    metricvals = [vals[subIDs.index(s)] for s in sids]

    width = 0.5
    fig, ax = subplots(2) #Create new empty plot with two subplots (we'll split data)
    idx = numpy.arange( len(sids)) #Indices on horizontal axis
    Nsplit = int(len(sids)/2)

    rects = ax[0].bar( idx[0:Nsplit], metricvals[0:Nsplit], width, yerr = metricuncs[0:Nsplit] ) #Create bar plot
    #Add info
    # ax[0].set_xlabel(xLabel)
    ax[0].set_ylabel(yLabel)
    ax[0].set_xticks( idx[0:Nsplit]+width/2.) #Make xticks for every bar, centered on bars
    ax[0].set_xticklabels( sids[0:Nsplit] , rotation = 'vertical')
    #Adjust ticks smaller for legibility
    ax[0].tick_params(axis='both', which='major', labelsize=8)
    ax[0].tick_params(axis='both', which='minor', labelsize=6)
    ax[0].set_xlim( idx[0], idx[Nsplit]) #Fix axis limits so we use the whole space
    #Add second plot
    rects = ax[1].bar( idx[Nsplit:], metricvals[Nsplit:], width, yerr = metricuncs[Nsplit:] ) #Create bar plot
    #Add info
    ax[1].set_xlabel(xLabel)
    ax[1].set_ylabel(yLabel)
    ax[1].set_xticks( idx[Nsplit:]+width/2.) #Make xticks for every bar, centered on bars
    ax[1].set_xticklabels( sids[Nsplit:] , rotation = 'vertical')
    ax[1].set_xlim( idx[Nsplit], idx[-1]+1) #Fix axis limits so we use the whole space
    #Adjust ticks smaller for legibility
    ax[1].tick_params(axis='both', which='major', labelsize=8)
    ax[1].tick_params(axis='both', which='minor', labelsize=6)

    # adjust subplot then save and close figure
    savefig(fileName) 
    plt.close(fig)


# DISCLAIMER: I am 100% there is a better way to do this than a for loop through all the data, probably something with comparing arrays, but I didn't want to take the time to figure it out when I first wrote this script
def Lipinski(calc, exp, low, high):
    """
    Input: listLike calculated and experimental data you want to compare
    float low and high limits for the test
    returns:
    number of correctly predicted values (in or outside range)
    number of false positives
    number of false negatives
    """
    correct = 0
    falsePos = 0
    falseNeg = 0
    for c,e in zip(calc, exp):
        # If the calculated value is in range
        if low <= c <= high:
            # If the experimental is in range then add to correct
            if low <= e <= high:
                correct += 1    
            else: # Otherwise it is a false positive
                falsePos += 1
        else: # c not in range
            # If experimental is in range then its a false negative
            if low <= e <= high:
                falseNeg += 1
            else: # Otherwise they're both out so it's correct
                correct += 1
    # Return number correctly predicted, number of false positives, number of false negatives
    return correct, falsePos, falseNeg

def getLipinskiData(calc, exp, dexp, lowLim, highLim, bootits):
    """
    Provide data in list like form for calculated value, experimental and experimental uncertainty
    Include range to find data and number of bootstrapping iterations
    Returns the number of correctly predicted items within provided range, number of false positives, number of false negatives and their associated uncertainties from bootstrapping.
    """
    # Get numbers for lipinski rule
    correct, falsePos, falseNeg = Lipinski(calc, exp, lowLim, highLim)
    # Initiate arrays to store bootstrap data
    corrs = np.zeros(bootits)
    Poss = np.zeros(bootits)
    Negs = np.zeros(bootits)

    # Do bootstrapping
    for it in range(bootits):
        # here
        [c, e] = bootstrap_exptnoise(calc, exp, dexp)
        corrs[it], Poss[it], Negs[it] = Lipinski(c, e, lowLim, highLim)
        # Return values and their corresponding uncertainties
    return [correct, corrs.std()], [falsePos, Poss.std()], [falseNeg, Negs.std()]

def JCAMDdict(w = 1, square = False):
    """
    This method returns a dictionary with the figure settings for JCMD, including font sizes and markersize defaults. Then you can edit the dictionary once you've called this method. 

    w should be 0 to 4 corresponding to [39, 84, 129, 174] mm figure width
    If square is true then the height and width will be equal, otherwise height will be determined as the golden ratio * width
    """
    # options for figure width on JCAMD in mm  
    widths = [39, 84, 129, 174, 267]
    # Convert width in mm to inches  
    wid = widths[w]* 0.0393701 # Convert to inches

    # Determine height
    if square:
        height = wid
    else:
        height = wid * (sqrt(5.0) - 1.0) / 2.0

    parameters =  {'backend': 'ps', 
            'axes.labelsize': 8,
            'font.size': 8,
            'xtick.labelsize': 8,
            'ytick.labelsize': 8,
            'figure.figsize': [wid, height], 
            'legend.fontsize': 8, 
            'font.family':'sans-serif', 
            'font.sans-serif':'arial',
            'lines.markersize': 3,
            'lines.linewidth': 0.25,
            'figure.autolayout' : False,
            'figure.subplot.right': 0.6,
            'figure.subplot.left': 0.15,
            'figure.subplot.bottom': 0.2,
            'figure.subplot.top': 0.85
            }

    return parameters
    
def getSlope(calc1, expt1, dexp1, bootits, noise = True):
    """
    Calculates the slope between calculated and experimental data assuming the experimental results are on the x-axis. 

    Uses bootstrapping to get uncertainty in this value
    """
    # make sure data is in an array formate for analysis
    calc = np.array(calc1, dtype = np.float64)
    expt = np.array(expt1, dtype = np.float64)
    exptunc = np.array(dexp1, dtype = np.float64)

    # switch axis for least squares method
    xtemp = expt[:,numpy.newaxis]
    # Use least squares method to calculate slope
    coeff,_,_,_ = numpy.linalg.lstsq(xtemp, calc)
    slope = coeff[0]
    
    # Repeat for each bootstrap iteration
    slopes = numpy.zeros(bootits)
    for it in range(bootits):
        if noise:
            [ c, e ] = bootstrap_exptnoise( calc, expt, exptunc)  #Generate new sets, adding appropriate random variation to the experimental set.
        else:
            [ c, e ] = bootstrap( [calc, expt] ) # Generate new sets without adding noise to the experimental set

        xtemp = e[:, numpy.newaxis]
        coeff,_,_,_ = numpy.linalg.lstsq(xtemp,c)
        slopes[it] = coeff[0]

    return [slope, slopes.std()]


def BoxWhiskerByBatch(M, batches, entry = {}, predLabel = None, title = "", xAxis = '',  bat_label = 'Batch', split = '_', fileName = 'boxplot.pdf', Datakey = 'data'): 
    """
    This creates box and whisker plots for a set of data in a dictionary assuming it is organized the same as dictionaries in the SAMPL5 challenge
    M = dictionary with data 
    batches = list of lists that has keys separated into batches
    
    entry = dictionary of predictions, if blank then no prediction is indicated on the plot
    title = string for plot title
    split = character to split front of keys word that is unwanted, if '' then whole key is used. 
    """
    # Get and adjust parameters for the plot
    parameters = JCAMDdict(3)
    parameters['figure.figsize'][1] *= 1.5
    parameters['figure.subplot.right'] = 0.95
    parameters['figure.subplot.left'] = 0.1
    parameters['figure.subplot.top'] = 0.95
    parameters['figure.subplot.bottom'] = 0.15
    rcParams.update(parameters)

    # Create figure and an axes for each batch
    fig, axes = subplots(len(batches), 1)
    fig.suptitle(title) # add title

    # Is there data in the dictionary?
    PredDataProvided = entry.has_key(Datakey)
    
    # Loop through batches
    for b, batch in enumerate(batches):
        hasPrediction = False
        ax = axes[b]
        # Sort keys in the batch
        keys = sorted(batch)

        # Make labels without SAMPL5 at the front
        labels = [k.split(split)[1] for k in keys]
        # preData data is a list of lists of all predicted values for that molecule
        preData = [M[k]['calc'] for k in keys] 

        # expData is a list of floats with the experimental result for that molecule
        e = np.array([M[k]['exp'][0] for k in keys])
        de = np.array([M[k]['dexp'][0] for k in keys])

        # Check if this prediction submitted data for this batch
        if PredDataProvided: 
            hasPrediction = entry[Datakey].has_key(keys[0])

        if hasPrediction:
            # Get prediction data for this batch:
            my = np.array([entry[Datakey][k][0] for k in keys])
            dmy = np.array([entry[Datakey][k][1] for k in keys])

        # Create boxplot
        # Folling histogram settings for multiple rows
        # default for whis is 1.5
        bp = ax.boxplot(preData, whis = 100.0)
        ax.set_ylabel('logD')
        ax.set_xticklabels(labels, rotation = 'vertical')

        # change line colors
        [fly.set(color = '#7570b3', marker = '.') for fly in bp['fliers']]
        [[box.set(color = '#7570b3') for box in bp[feature]] for feature in ['boxes','caps','medians','whiskers']]

        # Add Experimental Data
        for i in range(len(e)):
            # Get position on the x axis from the box and whisker plot
            Xs = np.average(bp['medians'][i].get_xdata())
            exp = ax.errorbar(Xs, e[i], yerr = de[i], fmt = 'ks', label = 'experimental', capsize = 0.5) 

            # Check if this prediction submitted data for this batch
            if hasPrediction:
                mine = ax.errorbar(Xs, my[i], yerr = dmy[i], fmt = 'ro', label = predLabel,  capsize = 0.5)

        pred = matplotlib.lines.Line2D([],[], color = '#7570b3', linestyle = 'dashed', label = 'predicted (all)')
        
        # Add label for which batch
        ax.text(0.02, 0.95, "%s %i" % (bat_label, b), transform = ax.transAxes, verticalalignment = 'top', bbox = dict(boxstyle = 'round', facecolor = 'white'))
        

    if PredDataProvided:
        axes[-1].legend(bbox_to_anchor = (0.5, -0.4), loc = 9, ncol = 3, borderaxespad = 0., handles = [pred, exp, mine])
    else:
        axes[-1].legend(bbox_to_anchor = (0.5, -0.4), loc = 9, ncol = 3, borderaxespad = 0., handles = [pred, exp])
    # turns off frame around figure, must be done after adding subplots 
    # fig.frameon = False 
    # Label X-axes 
    fig.text(0.5, 0.07, xAxis, ha = 'center')
    
    # Save plot and close figure
    print "making plot ",fileName
    savefig(fileName)
    plt.close(fig)
    # sys.exit(1)

