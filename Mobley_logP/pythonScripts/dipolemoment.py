#!/bin/env python


import openmoltools
from openeye.oechem import *
import os
import commands
import sys
# from mmtools.moltools.ligandtools import *
import pickle
import numpy
from numpy import *
import matplotlib
import pylab

#Load dictionary of compounds names
compoundlib = pickle.load(open("updatedsmiles.p",'rb'))

#Set path for location of mol2 files
SAMPLpath = "mol2files/%s.mol2"

#Function for computing mol2 file dipole moments
def get_mol2_dipole(mol2file):
    """Read specified mol2 file and return the dipole moment (in Debye) computed using the charges in the file, which are assumed to have units of the electron charge."""

    #Read file into text
    file = open( mol2file, 'r')
    text = file.readlines()
    file.close()

    #Extract atoms section
    atomstart = text.index('@<TRIPOS>ATOM\n')+1
    atomend = text.index('@<TRIPOS>BOND\n')
    atomsec = text[ atomstart:atomend]

    #Allocate storage for coordinates and charges
    natoms = len(atomsec)
    Pos = zeros( (natoms, 3), float)
    charge = zeros(natoms, float)

    #Extract coordinate and position info
    for (atom, line) in enumerate(atomsec):
        tmp = line.split()
        tmp = line.split()
        #Store coordinates
        for i in range(3):
            Pos[atom, i] = float( tmp[i+2] )
        #Store charge
        charge[atom] = float( tmp[8] )

    #Compute dipole moment
    dipole = zeros((3), float)
    for atom in range(natoms):
        dipole+= charge[atom] * Pos[atom,:]

    #Compute magnitude
    magnitude = sqrt( dot( dipole, dipole) )

    #Currently units are e*angstrom; convert to debye
    convfactor = 0.20822678 #1 debye is 0.208... e*nm
    magnitude_debye = magnitude/convfactor
    return magnitude_debye

# set max dipole
maxdip = 0

#Loop through compound library and calculate the dipole moment
for num in compoundlib.keys():
        location = SAMPLpath % num
        pol = get_mol2_dipole(location)
	# to see all compound samples with their dipole moments, uncomment the line below
        #print num, pol
	# if dipole greater than current max, replace max dipole value and identify the coupound as max solv
	if pol > maxdip:
		maxdip = pol
		maxsolv = num

print "Sample with maximum dipole: %s, Value: %s" % (maxsolv, maxdip)


