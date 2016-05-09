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
import pylab

def rmserr( set1, set2 ):
    """Compute and return RMS error for two sets of equal length involving the same set of samples."""
    tot = 0.
    for i in range(len(set1)):
        tot+= (set1[i] - set2[i])**2
    return sqrt(tot/float(len(set1)))



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

    #COMPUTE OVERALL PERFORMANCE
    #Compute various metrics -- average error, average unsigned error, RMS error, Kendall Tau, Pearson correlation coefficient
    # Percent Correct Sign
    # converter to numpy arrays (incase they weren't already)
    calc = np.array(calc1)
    expt = np.array(expt1)
    exptunc = np.array(exptunc1)
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
    maxE = abs(max(calc-expt))

    #DO BOOTSTRAP ERROR ANALYSIS FOR OVERALL PERFORMANCE
    print "   Bootstrap for %s..." % sid
    avgerrs = numpy.zeros( boot_its)
    RMSerrs = numpy.zeros( boot_its)
    AUEs = numpy.zeros(boot_its)
    taus = numpy.zeros(boot_its)
    Rs = numpy.zeros(boot_its)
    maxEs = numpy.zeros(boot_its)
    pers = numpy.zeros(boot_its)
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
        maxEs[it] = abs(max( e-c))
        pers[it] = CorrectSign(c, e)

    return [avgerr, avgerrs.std()], [RMS, RMSerrs.std()], [AUE, AUEs.std()], [tau, taus.std()], [R, Rs.std()], [maxE, maxEs.std()], [per, pers.std()] 

# Metho for making plots comparing calculated and experimental Data
def ComparePlot(x, y, Title, XLabel, YLabel, xerr, yerr, labels, fileName = None):
    """ Input:
        x, y, xerr, yerr = list of arrays to be plotted 
        Title, XLabel, YLabel = strings for labeling plot
        labels = list of labels for the legend
        fileName = string, optional, save plot to file
    
    """
    symbols = ['ro','bs','gD','rx','bo','gs']
    # adjustment so limits are aleast as big as error bars 
    adjust = max((max(max(xerr)), max(max(yerr)))) + 0.2
    expError = 1.0 # log units range to show

    # Set up so that multiple sets of data can be passed, so if only one set is passed make it a list of lists still
    try:
        len(x[0])
    except:
        x = [x]
        y = [y]
        xerr = [xerr]
        yerr = [yerr]
        
    # Find limits find the minimum and maximum of all data
    lowLim = min([min(min(x)), min(min(y))]) - adjust
    highLim = max([max(max(y)), max(max(x))]) + adjust
    
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
        p1 = ax1.errorbar(x[i],y[i], xerr = xerr[i], yerr = yerr[i], fmt = symbols[i], label = labels[i])
        handles.append(p1)

    # Insert range for "correct" prediction
    L = numpy.array([lowLim-20, highLim +20])
    ax1.plot(L,L, 'k-', markersize = 6.0)
    ax1.fill_between(L, L+expError, L-expError, facecolor = 'yellow', alpha = 0.5, label = "Agree within %.1f" % expError)
    yellow = patches.Patch(color = 'yellow', label = r'$\pm$ %0.1f log units' % expError)
    handles.append(yellow)

    ax1.legend(bbox_to_anchor = (1.02, 0.98), loc = 2, ncol = 1, borderaxespad = 0., handles = handles)

    if fileName != None:
        fig1.savefig(fileName, dpi = 1200, bbox_inches = 'tight', pad_inches = 0.5, orientation = 'landscape')

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

def makeQQplot(X, Y, slope, title, xLabel ="Expected fraction within range" , yLabel ="Fraction of predictions within range", fileName = None, uncLabel = 'Mobdel Unc.'):
    """
    Provided with experimental and calculated values (and their associated uncertainties) in the form of list like objects. 

    Provides the analysis to make a QQ-plot using the guassian integral methods David wrote for SAMPL4 that are included above.

    Makes a files of the plot and returns the "error slope" as a float and the figure of the created plot
    """
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
    handles = [p1,p2,p3]
    ax1.legend(bbox_to_anchor = (1.02, 0.98), loc = 2, ncol = 1, borderaxespad = 0.)
    
    if fileName != None:
        fig1.savefig(fileName, dpi = 1200, bbox_inches = 'tight', pad_inches = 0.5, orientation = 'landscape')
    plt.close(fig1)

def histPlot(subIDs, vals, dvals, xLabel, yLabel, title, option = None, fileName = None, absolute = True):
    """"
    Makes histogram plots of data at IDs with sorted data. Provide settings for plot, including labels and titles. Saved out to fileName. 
    option is the way the data should be sorted, if None it is from smallest to largest vals the other options are reverse (or from largest to smallest vals) or 'close to 1' which sorts based on which value is closest to one.
    """
    if absolute:
        temp = zip(subIDs, abs(array(vals)), dvals)

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

    else: # No absolute value:
        temp = zip(subIDs, array(vals), dvals)
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

    # "unzip" values and undo absolute value
    (sids, tempVals, metricuncs) = zip(*temp)
    metricvals = [vals[subIDs.index(s)] for s in sids]

    width = 0.5
    fig, ax = pylab.subplots(2) #Create new empty plot with two subplots (we'll split data)
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
    pylab.savefig(fileName) 
    plt.close(fig)

