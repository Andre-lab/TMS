import pandas as pd
import numpy as np
import glob

# Load likelihoods from iqtree
d = {'params':[],'mle':[]}
cmdfile = 'commands_resubmit'
n_fails = []
lengths = []
with open(cmdfile, 'w') as f_out:
    for q in glob.glob('q_matrices/*paml'):
        f = q.split('/')[-1][:-5]
        f = f'mles/{f}/{f}.mles'
        p = f.split('/')[-1].replace('.mles','')
        p = '_'.join(p.split('_')[1:])
        kappa = float(p.split('_')[3])

        try:
            df1 = pd.read_csv(f, delim_whitespace=True)
        except:
            n_fails.append(p)
            cmd = f'mkdir mles/E2Q_{p}; cd mles/E2Q_{p}; /home/norn/.conda/envs/rates/bin/python /home/norn/q_matrix/compute_mles_for_q_free_t.py --qmatrix /home/norn/q_matrix/q_matrices/E2Q_{p}.paml;cd /home/norn/q_matrix;'
            f_out.write(cmd + '\n')
            continue
        df1 = df1[df1['mle']!='fail']
        df1 = df1[df1['mle']!='mle']

        if len(df1)==52:
            mles = pd.to_numeric(df1['mle'])
            d['params'].append(p)
            d['mle'].append(np.mean(mles))
        else:
            n_fails.append(p)
            lengths.append(len(df1))
            cmd = f'mkdir mles/E2Q_{p}; cd mles/E2Q_{p}; /home/norn/.conda/envs/rates/bin/python /home/norn/q_matrix/compute_mles_for_q_free_t.py --qmatrix /home/norn/q_matrix/q_matrices/E2Q_{p}.paml;cd /home/norn/q_matrix;'
            f_out.write(cmd + '\n')

print(f'{len(n_fails)} commands failed')
df1 = pd.DataFrame.from_dict(d)
df1['N'] = df1['params'].str.split(pat='_',expand=True)[0]
df1['p_transition'] = df1['params'].str.split(pat='_',expand=True)[2]
df1['offset'] = df1['params'].str.split(pat='_',expand=True)[1]
df1['kappa'] = df1['params'].str.split(pat='_',expand=True)[3]

df1.to_csv('mles_and_params.csv')
