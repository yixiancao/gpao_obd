from turtle import mode
import template
from astropy.units import degree, arcmin, arcsec
from astropy.coordinates import SkyCoord

def generate_lgs_vis_template(target, usename = False):
    tel = SkyCoord(target['ra']*degree, target['dec']*degree)

    tel_alpha, tel_delta = template.coord_to_alpha_delta(tel)

    mode = "LGS_VIS"
    ngs_source = "SCIENCE"
    lgs_source = "SCIENCE"
    sts_offset = "10.0"

    if usename:
        obname = f"{mode}_{target['name']}".replace(' ', '_')
    else:
        obname = f"{mode}_{tel_alpha.split('.')[0]}{tel_delta.split('.')[0]}_{target['Grp']:4.1f}_{target['K']:4.1f}".replace(' ', '_')

    replace = {'OBNAME'         : obname,
            'TEL.TARG.NAME'     : f"{target['name']}",
            'TEL.TARG.ALPHA'    : tel_alpha,
            'TEL.TARG.DELTA'    : tel_delta,
            'TEL.TARG.PARALLAX' : f"{target['parallax']/1e3:.6f}",
            'TEL.TARG.PMA'      : f"{target['pmra']/1e3:.6f}",
            'TEL.TARG.PMD'      : f"{target['pmdec']/1e3:.6f}",
            'TEL.TARG.MAG.K'    : f"{target['K']:.1f}",
            'COU.AO.TYPE'       : mode,
            'COU.NGS.SOURCE'    : ngs_source,
            'COU.NGS.NAME'      : f"{target['name']}",
            'COU.NGS.ALPHA'     : "0",
            'COU.NGS.DELTA'     : "0",
            'COU.NGS.PARALLAX'  : "0",
            'COU.NGS.PMA'       : "0",
            'COU.NGS.PMD'       : "0",
            'COU.NGS.MAG'       : f"{target['Grp']:.1f}",
            'COU.NGS.WLENGTH'   : "800.0",
            'COU.LGS.SOURCE'    : lgs_source,
            'ISS.STS.OFFSETDIST': sts_offset,
    }

    template.generate(replace)
    print (f"template generated at {replace['OBNAME']}.obd")
    return