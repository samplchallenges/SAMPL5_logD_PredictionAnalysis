#Concatentate xvg files that were started without appending
import commands as c
import os
import sys
import pickle
import numpy
import glob
from fixXVG import *


sampl = pickle.load(open("updatedsmiles.p",'rb'))
xvgPath = "/work/cluster/burleyk/RotationProject/SAMPL_Data_Fall2015/%s/%s/calculation/"

#Loop through folders that were run using updatedsmiles
for solv in ['cyclohexane','water']:
    for num in sampl.keys():
        path = xvgPath % (solv, num)
        i = 0
        while (i<20):
            #identify original prod.*.xvg file
            xvgfil = "%sprod.%s.xvg" % (path, i)
            #create header file from original prod.*.xvg file 
            
            #identify non-appended xvg file
            findxvg2 = glob.glob('%sprod2.%s.part*.xvg' % (path,i))
            print 'Found appended file for %s, %s' % (findxvg2, i)
            
            #if non-appended exists, genfromtxt and delete repeated times
            if findxvg2:
                #use Caitlin's methods to fix files and combine
                newxvg = CombineXVG(xvgfil, findxvg2[0], '%stotalprod.%s.xvg' % (path, i))
                print 'Found %s and combined with %s' % (findxvg2, xvgfil)

            else:
                #if no additional xvg file, gen orignal xvg from text and keep all lines
                print 'No additional xvg files for %s %s Lamda %s' % (solv, num, i)
                newxvg = removeCorruptLines (xvgfil)
                c.getoutput('cp -v %s %stotalprod.%s.xvg' % (xvgfil, path, i))
            #move to next numbered prod file 
            i = i + 1

  
        
