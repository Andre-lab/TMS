# TMS

analysis.ipynb
---------------------------------------------------------
This notebook contains all the code to make all analysis
presented in the paper. You can rerun this analysis
using precomputed data provided. 

rosetta_energy_scans/
---------------------------------------------------------
Energies computed with Rosetta for all amino acids at all 
positions for 52 of high-resolution experimental proteins 
structures.

msa/
---------------------------------------------------------
pfam seed alignments for the same set of proteins. This 
folder also contains a phylogenetic tree for each 
alignment computed with IQTREE:
bash msa/find_LG_mles.sh

q_matrices/
---------------------------------------------------------
TMS matrices computed over various hyperparameters
based on grid-search. To recompute parameter grid-search
run:
bash scripts/00_make_cmds_for_grid_optimization.sh
the script only creates the commands. You will have
to execute them yourself (requires >5k CPU hours).

mles/
-------------------------------------------------------
Contains a file for each q matrix with logLs for each 
alignments. To make cmds for recompute those run
python scripts/make_Q2logL_cmds.py
(requires >5k CPU hours)
