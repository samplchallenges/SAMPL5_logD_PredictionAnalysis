import pickle

testStats = pickle.load(open('testStats.p','rb'))
metrics  = ['AveErr','RMS','AUE','tau','R','maxErr','percent','error slope']
keys = ['1b3d','a4dd','602e','c410','232e'] 
pm = u"\u00B1"
pm = " +/- "
kList = 'key\t\t\t\t'+' \t\t\t\t\t'.join(keys)
for met in metrics:
    print met
    print kList
    for end in ['_un','_low','_high']:
        metList = []
        for k in keys:
            key = k+end
            metList.append("%.2f%s%.3f" % (testStats[key][met][0], pm, testStats[key][met][1]))
        if end == '_high':
            print end.replace('_','') + "\t\t\t" + "\t\t\t".join(metList)
        else:
            print end.replace('_','') + "\t\t\t\t" + "\t\t\t".join(metList)

    print
    print

