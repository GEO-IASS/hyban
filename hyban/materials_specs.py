#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from utils import read_hyper, make_rgb8

# -- get a representative frame
def get_frame_norm(lam=550.):
    """
    Get a normalized frame at some wavelength lambda.
    """
    fr = cube.data[np.abs(cube.waves - lam).argmin()]

    return fr / float(fr.max())

# -- utilities
dpath = os.path.join("..", "data")
rname = "veg_00945.raw"
fname = os.path.join(dpath, rname)
icol  = 605
rr    = (1175, 1350)

# -- read the cube
cube = read_hyper(fname)

# -- get the spectra
specs = cube.data[:, rr[0]:rr[1], icol].T.copy()

# -- get the mean spectrum
mspec = specs.mean(0)

# -- regress out that spectrum from each
cc  = np.array([np.polyfit(mspec, 1.0 * i, 1) for i in specs])
mod = (cc[:, 1] + cc[:, 0] * mspec[:, np.newaxis]).T
res = specs - mod

# -- get the RGB image
rgb  = make_rgb8(cube.data, cube.waves, scl=5.)
rgb2 = make_rgb8(cube.data, cube.waves, scl=2.5)

# -- make some plots
figure(1)
clf()
imshow(res, aspect=2, cmap="viridis", clim=(-30, 30))

figure(2, figsize=(5 / 0.45, 5))
subplots_adjust(0, 0, 1, 1)
clf()
axis("off")
xlim(409, 832)
ylim(1509, 1086)
imshow(rgb, aspect=0.45)

figure(3, figsize=(5 / 0.45, 5))
subplots_adjust(0, 0, 1, 1)
clf()
axis("off")
imshow((rgb2/255.)**0.75, aspect=0.45)

