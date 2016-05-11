import pickle
from sigfig.sigfig import *
import numpy as np

data = pickle.load(open('dictionary_withpKas.p','rb'))
pH = 7.4

output = ['SAMPL ID, "logP", acid corrected, base corrected, largest correction\n']
for k in sorted(data.keys()):
    e = data[k]
    pKaAcid = e['pKa_acidic']
    pKaBase = e['pKa_basic']
    if pKaAcid == None:
        acid_correction = 0
    else:
        acid_correction = 10**(pH - pKaAcid) 
    if pKaBase == None:
        base_correction = 0
    else:
        base_correction = 10**(pKaBase - pH)

    logP = (e['LogD_calc'][0])
    P = 10 ** logP
    dlogD = e['LogD_calc'][1]
    
    aD = P / (acid_correction + 1)
    bD = P / (base_correction + 1)
    bothD = P / (acid_correction + base_correction + 1)

    aLogD = np.log10(aD)
    bLogD = np.log10(bD)
    bothLogD = np.log10(bothD)
    oneLogD =min([aLogD, bLogD, logP]) 
    output.append('%s,\t\t%s,\t\t%s,\t\t%s,\t\t%s\n' % (k, round_unc(logP, dlogD), round_unc(aLogD, dlogD), round_unc(bLogD, dlogD), round_unc(oneLogD, dlogD)))

    e['LogD_acidCorrected'] = [aLogD, dlogD]
    e['LogD_baseCorrected'] = [bLogD, dlogD]
    e['LogD_bothCorrected'] = [bothLogD, dlogD]
    # This assumes the molecule is either an acid or a base, but not both, takes the biggest change 
    e['LogD_oneCorrected'] = [oneLogD, dlogD]

pickle.dump(data, open('dictionary_pKaCorrected.p','wb'))
F = open('allLogD_pKacorrectedData.txt', 'w')
F.writelines(output)
F.close()
