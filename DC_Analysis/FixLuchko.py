# Written by Cailtin C Bannan
# Mobley Group, UC Irvine
# Tyler Luchko from CSU-Northridge made a human error in caclulating logD with a transfer free energy from cyclohexane to water instead of water to cyclohexane
# Since this is a minor human error and not an error in their protocol or methods, we decided to fix the sign on their logD for evaluation

import pickle
import glob

# Luchko's submissions
numbers = [5, 7, 17, 29, 35, 46, 71]
numbers = [9]
# get SID
numToSID = pickle.load(open('numToSID.p','rb'))

for num in numbers:
    # Get original ID number
    sid = numToSID[num]
    # Find file
    fileName = glob.glob("../predictionFiles/%s-282-*.txt" % sid)[0]
    # Read lines
    f = open(fileName, 'r')
    lines = f.readlines()
    f.close()
    # Make outputlines
    output = []

    for l in lines:
        # If it's a data line, multiply logD value by -1
        if l.split('_')[0] == 'SAMPL5':
            data = [i.strip() for i in l.split(',')]
            data[1] = str(float(data[1]) * -1)
            output.append(', '.join(data)+'\n')
        # Otherwise just add line as is to output file
        else:
            output.append(l)
    
    # Save new file here, then I will manually move them into the predictions directory
    newFileName = fileName.split('/')[-1]
    f = open(newFileName,'w')
    f.writelines(output)
    f.close()
