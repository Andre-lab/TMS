for msa in msa/*.phylip; do
	mle=$(/home/norn/software/iqtree-1.6.12-Linux/bin/iqtree -s $msa -st AA -m LG+FO+G4 -te $msa.treefile -pre LG -redo | grep "BEST SCORE FOUND" | awk '{print $NF}')
	echo $msa $mle
done
