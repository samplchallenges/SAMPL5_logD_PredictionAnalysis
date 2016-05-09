#!/bin/env python
# This was used to make the original index_table.csv with an old version of the dictionary. 

import pickle
import os

#Build a csv file listing submission number and other details so people can tell which one they are

#Load database
database = pickle.load(open('../DataFiles/predictions.p','rb'))

#Output text headers
outtext = ['Submission #, Method Name, Submitter, File Name\n']

#Loop over ID numbers and store to table
for nr in range(0,77):
    #Loop over database keys and find the one with this number
    for key in database.keys():
        if int(database[key]['number'])==nr:
            isAnonymous = database[key]['isAnonymous']
            #Store line
            if not isAnonymous:
                outtext.append( '%s, %s, %s %s, %s\n' % (nr, database[key]['name:'][0],database[key]['firstName'], database[key]['lastName'],  os.path.basename(database[key]['fileName']).split('-DC-')[1] ) )
            else:
                outtext.append( '%s, %s, Anonymous, ---\n' % (nr, database[key]['name:'][0] ) )
            break


file = open('index_table.csv', 'w')
file.writelines(outtext)
file.close()

