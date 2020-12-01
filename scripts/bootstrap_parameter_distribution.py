import numpy as np
import pandas as pd

df_mles = pd.read_csv('mles_all_trees_all_parameters.csv')
df_mles['params'] = df_mles['offset'].astype(str) + '_' + df_mles['N'].astype(str) + '_' + df_mles['p_transition'].astype(str) + '_' + df_mles['kappa'].astype(str)
d = {'offset':[], 'N':[], 'p_transition':[], 'kappa':[]}
param_list = ['offset','N','p_transition','kappa']
sample_size = 52

# What are the parameter combinations searched during grid optimization?
uniq_params = list(set(df_mles['params']))

# Which alignments did we calculate MLE for?
alns = list(set(df_mles['msa']))

# Select a random subset from those alignments for the bootstrap
subset = np.random.choice(alns, size=sample_size, replace=True)
dfsub = df_mles[df_mles['msa'].isin(subset)]
g = dfsub.groupby('params')

# For each parameter combination, compute the mean MLE for the selected subset of alignments
mles = []
for param in uniq_params:
    mle = g.get_group(param)['mle'].mean()
    mles.append(mle)

# Find the idx for the highest MLE parameter combination and print that
best_param = uniq_params[np.argmax(mles)]
vals = [float(x) for x in best_param.split('_')]
_ = [d[k].append(v) for k,v in zip(d.keys(), vals)]
print(best_param.replace('_',' '))



