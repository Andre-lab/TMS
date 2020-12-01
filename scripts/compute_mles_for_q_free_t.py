import glob
import subprocess
from optparse import OptionParser
import os, re
import pandas as pd
import shutil 

# Signal handling
import signal
def signal_handler(sig, frame):
    print('caught termination signal. Cleaning up')
    shutil.rmtree('msa')
signal.signal(signal.SIGTERM, signal_handler)


parser = OptionParser(usage="usage: %prog [options] FILE", version="0.1")
parser.add_option("--qmatrix", type="string", dest="qmatrix", metavar="STR", help="Input q matrix")
(opts, args) = parser.parse_args()

exe = '/home/norn/software/iqtree-1.6.12-Linux/bin/iqtree'
qmatrixPath = opts.qmatrix
qmatrixName = qmatrixPath.split('/')[-1].replace('.paml','')
output_f = qmatrixName + '.mles'
print('will write to ', output_f)

# Checkpointing
seen_msas = []
if os.path.exists(output_f):
    try:
        df_checkpoint = pd.read_csv(output_f, delim_whitespace=True)
        df_checkpoint = df_checkpoint.dropna()
        df_checkpoint = df_checkpoint[df_checkpoint['mle']!='fail']
        seen_msas = list(df_checkpoint['msa'])
        print("loaded from checkpoint")
    except:
        print("Did not load from checkpoint")

# we need to copy the msa dir because of checkpointing by iqtree
if not os.path.isdir('msa'):
    shutil.copytree('/home/norn/q_matrix/msa_small', 'msa')

with open(output_f,'a') as f_out:
    if len(seen_msas)==0:
        f_out.write('msa mle\n')
    for msa in glob.glob('msa/*.phylip'):
        if msa in seen_msas:
            continue
        if qmatrixPath=='LG':
            cmd = f'{exe} -s {msa} -st AA -m {qmatrixPath}+FO+G4 -t {msa}.treefile -redo --no-outfiles | grep "BEST SCORE FOUND"'
        else:
            cmd = f'{exe} -s {msa} -st AA -m {qmatrixPath}+FO+G4 -t {msa}.treefile -redo --no-outfiles | grep "BEST SCORE FOUND"'
        print(cmd) 
        try:
            output = subprocess.check_output(cmd, shell=True).decode("utf-8").strip().split(' ')[-1]
        except subprocess.CalledProcessError as exc:
            output = 'fail'
            print("Status : FAIL", exc.returncode, exc.output)

        out_s = msa + ' ' + output + '\n' 
        f_out.write(out_s)
        f_out.flush()
        os.fsync(f_out)

# Clean-up
shutil.rmtree('msa')

