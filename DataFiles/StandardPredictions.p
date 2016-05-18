(dp0
S'56b0df26da016'
p1
(dp2
S'longID'
p3
g1
sS'methodNum'
p4
S'1'
p5
sS'method:'
p6
(lp7
S'Distribution coefficients were estimated from the difference in solvation free energies of the neutral solute into cyclohexane and water. Solvation free energies were calculated in explicit solvent with GROMACS in the generalized amber force field (GAFF) and AM1-BCC charges.'
p8
aS'The Solvation Toolkit (using Packmol, OpenMolTools, AmberTools and ParmEd) was used to build input files for each of the solutes in cyclohexane and water from the provided SMILE strings. The number of solvent molecules were chosen such that the box edge was at least 3 nm (1000 TIP3P water molecules or 500 cyclohexane molecules). Solvation free energies were calculated at infinite dilution so only 1 solute molecule was included.'
p9
aS'Generally protocols were taken from previous work with relative solubility calculations in our group and updated to work with GROMACS 5.0.4. The alchemical solvation was broken into 20 lambda states. In the first 5 lambda states the electrostatic interactions between the solute and solvent were turned off. Then the Van der Waals interactions (modeled by Lennard Jones potentials) were switched off in the last 15 lambda states. Each state was minimized using GROMACS steepest decent algorithm and then equilibrated for a total of 150ps. The equilibration was broken into three steps: (1) 50ps constant volume, (2) 50ps constant pressure with the Berendsen barostat, and (3) 50ps constant pressure with the Parrinello-Rahman barostat.  These were followed by a 5ns production phase at each lambda state, still using the Parrinello-Rahman barostat. The initial 100ps of the production stage was thrown out to give the system extra time to reach equilibrium.'
p10
aS'The free energy difference between each lambda value and the total solvation free energy was calculated using the Multistate Bennett Acceptance Ratio (MBAR) through the Alchemical Analysis tool. This included a statistical uncertainty of the solvation free energy which was propagated to get the statistical uncertainty in the logarithm of the distribution coefficient. The model error was taken as the RMS error of a previous study of partition coefficients between water and cyclohexane.'
p11
aS'We are continuing to explore issues of convergence of the larger molecules in this set.'
p12
asS'fileName'
p13
S'56b0df26da016-282-DCStandard-MobleySAMPL-1.txt'
p14
sS'data'
p15
(dp16
S'SAMPL5_059'
p17
(lp18
F-0.66
aF0.03
aF1.4
asS'SAMPL5_037'
p19
(lp20
F-4.68
aF0.03
aF1.4
assS'software:'
p21
(lp22
S'GROMACS 5.0.4'
p23
aS'OpenMolTools 0.6.9'
p24
aS'SolvationToolkit (downloaded September 30, 2015)'
p25
aS'PackMol 15.287'
p26
aS'mdtraj 1.4.2'
p27
aS'OpenEye tools 2015.Oct.1 release'
p28
aS'ParmEd 2.0.4'
p29
aS'Pymbar 3.0.0'
p30
asS'name:'
p31
(lp32
S'Solvation/GAFF/TIP3P/neutral'
p33
ass.