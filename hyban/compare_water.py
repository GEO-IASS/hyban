#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from utils import *

# -- set the indices for comparison
ind = np.array([411, 452, 493, 534])

# -- get scan conditions
sc = get_scan_conditions().iloc[ind]

# -- read in the scans
cubes = [read_hyper(os.path.join("..", "data", i)) for i in sc.filename]

# -- get rgb images
print("generating rgbs...")
rgbs = [make_rgb8(i.data, i.waves) for i in cubes]

# -- rescale rgb
#rescale = lambda rgb, scl, off: (rgb * scl + off).clip(0,255).astype(np.uint8)
rescale = lambda rgb: (255.*(rgb - rgb.min())/float(rgb.max() - rgb.min())) \
    .clip(0,255).astype(np.uint8)

# -- plot the four scans
rr   = [1110, 1460]
cc   = [1355, 1430]
rect = plt.Rectangle((cc[0], rr[0]), cc[1] - cc[0], rr[1] - rr[0], ec="lime", 
                     fc="none", lw=0.5)
scls = [1.0, 5.0, 5.0, 1.0]
fig, ax = plt.subplots(2, 2, figsize=(10, 5))
fig.subplots_adjust(0.05, 0.05, 0.95, 0.95)
dum     = [i.axis("off") for j in ax for i in j]
dum     = [i.imshow(j, aspect=0.45) for i, j in 
           zip([n for m in ax for n in m], 
               [rescale(rgb) for rgb in rgbs])]
dum     = [i.set_title(j) for i, j in 
           zip([n for m in ax for n in m], sc.time)]
ax[0, 1].add_patch(rect)
fig.canvas.draw()
fig.savefig("../output/scan_examples.png", clobber=True)


# -- get the spectra
specs = [i.data[:, rr[0]:rr[1], cc[0]:cc[1]].mean(-1).mean(-1) for i in cubes]

# -- normalize the water line
srng = [505, 530]
co   = [(1.0, 0.0)] + [np.polyfit(i[srng[0]:srng[1]], 
                                  specs[0][srng[0]:srng[1]], 1) 
                       for i in specs[1:]]

# -- make the plot
fig2, ax2 = plt.subplots()
lins = [ax2.plot(cubes[0].waves * 1e-3, j[0]*i + j[1])[0] for i, j in 
        zip(specs, co)]
labs  = ["1 day before", "rain day", "1 day after", "2 days after"]
ax2.set_xlabel("wavelength [micron]")
ax2.set_ylabel("intensity [arb units]")
ax2.grid(1)
ax2.legend(lins, labs)
fig2.canvas.draw()
fig2.savefig("../output/spec_examples.png", clobber=True)
