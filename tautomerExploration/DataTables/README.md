# Data Tables for Tautomer and pKa Correction analysis

This directory includes all data tables related to correcting calculated logP to logD using calculated pKas or state penalties for tautomer enumeration

Types of corrections include, acidic pKa, basic pKa, largest pKa (either acidic or basic that makes the biggest change), Epik state penalty (calculated using the Schrodinger ligprep and Epik tools), Pickard state penalty (use tautomer corrections provided by Frank Pickard)

* allLogDs.txt: This is a large table of logD values for each correction including the original logP and the experimental value (allLogD_pKacorrectedData.txt: includes only the pKa corrections)
* ErrorAnalysis_LogDCorrections.txt: Includes all error metrics for all correction types. It also includes data for our original logP calculations and those submitted by Andreas Klamt calculated with COSMO-RS (prediction set 16 which did the best by most error metrics in the SAMPL5 challenge). Also included here are "limited" errormetrics which are those where only logDs that are different from logP were included in the error analysis
penalties_fromPickard.txt: These are energy penalties provided by Frank Pickard for each molecule
* ComparingPenalties: This is a table of state penalties calculated by Frank Pickard and those we calculated using Schrodinger's Epik
* pKa_first.txt: These are the largest basic pKa or smallest acidic pKa, which dictate the first protonation or deprotonation.
* pKa_all.txt: This table includes lists of all acidic and basic pKa values for each molecule
* CompareTo16_0.0100.txt: This is another error analysis table where limited indicates changes in logP to logD that are at least 0.01 log units
* pdf files were created to help view tables while thinking about results, they are not final and were created by loading these txt files into excel. 

