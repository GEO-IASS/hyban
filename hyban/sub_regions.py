#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from utils import read_hyper, read_header

def get_patch_spectra(fname, rr, cr):
    """
    Get the patch spectra.

    :param fname:
        The name of the data cube (e.g., data.raw).

    :param rr:
        List of tuples containing the upper and lower row boundaries for 
        the regions.

    :param cr:
        List of tuples containing the upper and lower columen boundaries for 
        the regions.
    """

    # -- read the data cube
    cube = read_hyper(fname)

    # -- loop through patches and get spectra
    print("getting patch spectra...")
    nreg  = len(rr)
    specs = np.array([cube.data[:, rr[i][0]:rr[i][1], cr[i][0]:cr[i][1]] \
                          .mean(-1).mean(-1) for i in range(nreg)])

    return specs


if __name__=="__main__":

    # -- define the dates 
    #    May 31, June 2, 4, 6  11:00
    #    April 6th, 5pm
    dpath  = os.path.join("..", "data")
    flist  = [os.path.join(dpath, i) for i in 
              ["veg_00945.raw", "veg_01027.raw", "veg_01109.raw", 
               "veg_01191.raw"]]
    flist += [os.path.join(os.path.expanduser("~"), "vnir_new", 
                           "040616_full-0001.raw")]
    dates  = ["053116_1100", "060216_1100", "060416_1100", "060616_1100", 
              "040616_1700"]

    # -- define the regions
    rr = ((996, 1015), (1016, 1035), (1036, 1055), (996, 1015), (1016, 1035), 
          (1036, 1055), (996, 1015), (1016, 1035), (1036, 1055), (996, 1015), 
          (1016, 1035), (1036, 1055), (1135, 1150))
    cr = ((802, 812), (802, 812), (802, 812), (813, 823), (813, 823), 
          (813, 823), (824, 834), (824, 834), (824, 834), (835, 845), 
          (835, 845), (835, 845), (978, 994))

    # -- get the wavelengths
    waves = read_header(flist[0].replace("raw", "hdr"))["waves"]

    # -- get patch spectra
    for ii in range(len(flist)):
        specs = get_patch_spectra(flist[ii], rr, cr)
        oname = os.path.join("..", "output", "{0}_regs.csv".format(dates[ii]))
        np.savetxt(oname, np.vstack([waves, specs]).T, delimiter=",")
