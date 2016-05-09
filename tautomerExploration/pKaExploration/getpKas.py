import glob
import sys
import pickle

def dataline(line):
    try:
        data = line.split(' ')
        pKa = float(data[2])
        return True, data[1].strip(), pKa
    except:
        return False, None, None

dictionary = 'dictionary_allResults.p'
database = pickle.load(open(dictionary,'rb'))
Logs = glob.glob("MoleculeFiles/*_allpKa.log")

# Add keys to dictionary:
for k,e in database.items():
    e['Conj_Base'] = []
    e['Conj_Acid'] = []

for f in Logs:
    print f
    num = f.split('_')[1]
    samplID = 'SAMPL5_'+num
    # load lines from file
    fil = open(f)
    lines = fil.readlines()
    fil.close()
    # Find the line with Atom    Acid/Base    pKa    
    for i in range(len(lines)):
        line = lines[i].strip().replace('   ',' ')
        line = line.replace('  ',' ')
        isData, key, pKa = dataline(line)
        if isData:
            # print samplID, i, line
            database[samplID][key].append(pKa)

# Make lists to save data to write to txt file
relevant = ['SAMPL ID, acidic_pKa, basic_pKa \n']
allpKa = ['SAMPL ID, [all acidic_pKa], [all basic_pKa] \n']

# Save data
for k,e in database.items():
    if not e['Conj_Acid']:
        e['pKa_acidic'] = None
    else:
        e['pKa_acidic'] = min(e['Conj_Acid'])

    if not e['Conj_Base']:
        e['pKa_basic'] = None
    else:
        e['pKa_basic'] = max(e['Conj_Base'])

    info = '%s, %s, %s' % (k, str(e['pKa_acidic']), str(e['pKa_basic']))
    allInfo = "%s, %s, %s" % (k, str(sorted(e['Conj_Acid'])), str(sorted(e['Conj_Base'], reverse = True)))
    print info
    relevant.append(info+'\n')
    print allInfo
    allpKa.append(allInfo+'\n')

fN = open('pKa_first.txt', 'w')
fN.writelines(relevant)
fN.close()

fN = open('pKa_all.txt', 'w')
fN.writelines(allpKa)
fN.close()

pickle.dump(database, open('dictionary_withpKas.p','wb'))

