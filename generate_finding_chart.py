# %%

from glob import glob
from io import BytesIO
import re
import os
import requests
from matplotlib import pyplot
import numpy as np

from astropy.coordinates import SkyCoord
from astropy.units import degree, arcsec
from astropy.table import Table

import template

# %%

def parse_obd(filename):
    obd = {}
    with open(filename) as f:
        for line in f:
            if result := re.search(r'^(?P<key>\S+)\s+"(?P<value>\S+)"', line):
                obd[result.group('key')] = result.group('value')
    return obd

# %%

for filename in glob('*GS*.obd'):
    if not os.path.exists(filename.replace(".obd", ".png")):
        obd = parse_obd(filename)
        tel = SkyCoord(template.hms2deg(obd['TEL.TARG.ALPHA'])*degree, template.dms2deg(obd['TEL.TARG.DELTA'])*degree)
        ra = tel.ra.to(degree).value
        dec = tel.dec.to(degree).value
        radius = (60*arcsec).to(degree).value

        resp = requests.get(f'https://gsss.stsci.edu/webservices/vo/CatalogSearch.aspx?RA={ra:.6f}&DEC={dec:.6f}&SR={radius:.3f}')
        tbl = Table.read(BytesIO(resp.content))

        fig, axarr = pyplot.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)
        for i, mag_name in enumerate(['gaiaRpMag', 'tmassKsMag']):
            mag = tbl[mag_name]

            mag2size = lambda mag: 50*(np.max(mag)-mag)/(np.max(mag)-np.min(mag))
            size2mag = lambda size: np.max(mag)-(size/50)*(np.max(mag)-np.min(mag))

            axarr[i].plot(ra+10/3600*np.cos(np.linspace(0, 2*np.pi, 1000)), dec+10/3600*np.sin(np.linspace(0, 2*np.pi, 1000)), 'k', lw=1)
            axarr[i].plot(ra+ 5/3600*np.cos(np.linspace(0, 2*np.pi, 1000)), dec+ 5/3600*np.sin(np.linspace(0, 2*np.pi, 1000)), 'k', lw=0.5)
            data = axarr[i].scatter(tbl['ra'], tbl['dec'], mag2size(tbl[mag_name]))
            axarr[i].set_aspect('equal')
            axarr[i].legend(*data.legend_elements(prop='sizes', num=5, func=size2mag), title=mag_name, loc='upper right')
            axarr[i].set_xlim(ra-20/3600, ra+20/3600)
            axarr[i].set_ylim(dec-20/3600, dec+20/3600)
            fig.savefig(filename.replace(".obd", ".png"))
        pyplot.show()

# %%