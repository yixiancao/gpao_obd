import re
from pathlib import Path

def generate(replace):
    """
    Generate a new OB from template.obd

    Parameters
    ----------
    replace : dict
        dictionary with keyword value pairs to replace in template.obd
    
    Raises
    ------
    ValueError
        when not all replacement keywords are provided

    """

    # Read template.obd
    template_path = Path(__file__).parent / 'template.obd'

    with open(template_path, 'r') as f:
        ob = f.read()

    # Perform all replacements of <entries>
    for key, value in replace.items():
        ob = ob.replace(f"<{key}>", value)

    # Check that all replacements are performed
    if matches:=re.findall('<.*>', ob):
        matches = '\n'.join(matches)
        raise ValueError(f'Missing replacements:\n{matches}')

    # Save new ob
    with open(f"{replace['OBNAME']}.obd", 'w') as f:
        f.write(ob)


def coord_to_alpha_delta(coord):
    """
    Convert astropy SkyCoord to ESO format

    Parameters
    ----------
    coord : SkyCoord
        input coordinates

    Returns
    -------
    alpha : string
        Right ascension in ESO format [HHMMSS.sss]
    delta : string
        declination in ESO format [+DDMMSS.sss]

    """

    alpha, delta = coord.to_string('hmsdms').split()
    alpha = alpha.replace('h', '').replace('m', '').replace('s', '')
    delta = delta.replace('d', '').replace('m', '').replace('s', '')
    alpha_hi, alpha_lo = alpha.split('.')
    alpha = '.'.join([alpha_hi, alpha_lo[:3]])
    delta_hi, delta_lo = delta.split('.')
    delta = '.'.join([delta_hi, delta_lo[:3]])
    return alpha, delta

def hms2deg(hms):
    if isinstance(hms, str):
        hms = float(hms)
    hms = f'{hms:013.6f}'
    h = float(hms[0:2])
    m = float(hms[2:4])
    s = float(hms[4:])
    deg = 360/24*(h+m/60+s/3600)
    return deg

def dms2deg(dms):
    if isinstance(dms, str):
        dms = float(dms)
    dms = f'{dms:+014.6f}'
    sign = float(f'{dms[0]}1')
    d = float(dms[1:3])
    m = float(dms[3:5])
    s = float(dms[5:])
    deg = sign*(d+m/60+s/3600)
    return deg
