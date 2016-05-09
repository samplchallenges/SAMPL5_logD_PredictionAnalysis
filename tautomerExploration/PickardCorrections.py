import pickle
import numpy as np
import glob

d = pickle.load(open('dictionary_statePenalty.p','rb'))
output = ['SAMPL ID, logP, basic pKa, acidic pKa, largest pKa, Epik penalty, Pickard penalty, experiment\n']
exp = pickle.load(open('../DataFiles/experimental.p','rb'))
pen = pickle.load(open('penaltyDictionary.p','rb'))

for samplID, e in d.items():
    # Get SAMPLId
    num = samplID.split('_')[-1]

    # Convert to log based correction:
    logPj = pen[num]['logPickard']

    # Update dictionary
    logP = d[samplID]['LogD_calc']
    logD = logP[0] + logPj
    d[samplID]['logD_PickardCorrected'] = [logD, logP[1]]
    data = samplID
    for k in ['LogD_calc', 'LogD_baseCorrected','LogD_acidCorrected','LogD_oneCorrected','logD_stateCorrected', 'logD_PickardCorrected']:
        data = data +', %.2f' % d[samplID][k][0]
    data = data + ', %.2f' % exp[samplID]['data'][0]
    print data
    output.append(data+'\n')

fN = open('allLogDs.txt','w')
fN.writelines(output)
fN.close()
pickle.dump(d, open('dictionary_statePenalty.p','wb'))
