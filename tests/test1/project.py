import time 

import numpy as np
from tqdm import tqdm

total = 1000
iter_tqdm = tqdm(range(total))
for i in range(total):
    iter_tqdm.set_description(f"x = {i/100}, sin = {np.sin(i/100):.4f}")
    time.sleep(1)