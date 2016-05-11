# Plots for Tautomer and pKa Corrections

This directory contains comparison and QQ plots for all of the pKa and tautomer enumeration corrections. 

Here are some descriptors that will make the file names more understandable
* original: refers to original logP calculations by the Mobley group
* Epik and Pickard: refer to state penalties calculated using Schrodinger's epik tool and those provided by Frank Pickard
* pKa_*: plots for that correction type with coloring based on batch
* *_logP: plots show original logP and the new logD
* *_limited: plots only include points where the logD is different from logP

Compare_changing_* were requested by David for his presentation at the D3R workshop 
* largepKa.pdf: has the original logP and the logD corrected by pKa (either acidic or basic which ever causes a bigger change)
* state.pdf: Shows pKa corrected logD and Epik state penalty logD 
* all.pdf: Shows original logP, pKa corrected and Epik state penalty corrected logD

