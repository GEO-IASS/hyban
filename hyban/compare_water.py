#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from utils import *

# -- set the indices for comparison
ind = np.array([100, 215, 256, 297])

# -- get scan conditions
sc = get_scan_conditions().iloc[ind]

# -- read in the scans
cubes = [read_hyper(os.path.join("..", "data", i)) for i in sc.filename]

# -- get rgb images
print("generating rgbs...")
rgbs = [make_rgb8(i.data, i.waves) for i in cubes]

# -- plot the three scans
fig, ax = plt.subplots(2, 2, figsize=(10, 5))
fig.subplots_adjust(0.05, 0.05, 0.95, 0.95)
dum     = [i.axis("off") for j in ax for i in j]
dum     = [i.imshow(j, aspect=0.45) for i, j in 
           zip([n for m in ax for n in m], rgbs)]
dum     = [i.set_title(j) for i, j in zip(ax, sc.time)]
fig.canvas.draw()
fig.savefig("../output/scan_examples.png", clobber=True)

# -- set the spatial indices
rr = [1110, 1460]
cc = [1355, 1430]

# -- get the spectra
specs = [i.data[:, rr[0]:rr[1], cc[0]:cc[1]].mean(-1).mean(-1) for i in cubes]

fig2, ax2 = plt.subplots()
[ax2.plot(cubes[0].waves * 1e-3, i) for i in specs]
ax2.set_xlabel("wavelength [micron]")
ax2.set_ylabel("intensity [arb units]")
ax2.grid(1)
fig2.canvas.draw()
fig2.savefig("../output/spec_examples.png", clobber=True)
