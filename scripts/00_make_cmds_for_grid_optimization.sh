for o in $(python -c "import numpy as np; [print(x) for x in np.arange(9, 18, 0.5)]"); do
      echo "python -u scans2rates_final_gridopt.py -g $o -m nopk > grid_$o.final_grid.log" >> commands
done
