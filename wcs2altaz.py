#! /usr/bin/env python3
# -*- coding:utf-8 -*-

""" *** wcs2altaz ***

Give filename of cloud cam image as well as RA and DEC of target from WCS of image
to get the Altitude and Azimuth of target point

TBD
----
- Improve!!

ChangeLog
-----------
- 20210108: Initial version
"""

import ephem
import astropy
from datetime import datetime
from pytz import timezone 
import pytz
import math

import argparse

__version__ = "20210108"
__author__ = "asmith"




siteGem = ephem.Observer()
siteGem.lat = '19.823506'
siteGem.lon = '-155.468914'
siteGem.elevation = 4218  # meters
siteGem.pressure = 617    # mBar
siteGem.temp = -3.4
siteGem.epoch = '2000'
utc = pytz.utc
hst = timezone("Pacific/Honolulu")


def main(args):

    #put time in the proper format
    image_dt = hst.localize(datetime.strptime(args.filename.split('.')[0],'%y%m%d-%H%M%S'))
    image_ut = image_dt.astimezone(utc)
    
    # set the observer date to the image's UT time
    siteGem.date = image_ut
    
    ## This next is a horizon correction. Because Gem is at a higher elevation we see futher below the 0degree horizon at sea level. So, for correct rise and set time for sun
    ## some geometry has to be done. Skycalc, which almanac uses, has a different version of this already built in. Without it, there's an 8.33 min difference.
    ## Skycalc uses horizon correction (radians) = sqrt(2*elevation/radiusofearth)
    ## This is geometricaly similar
    
    hza = - math.acos(ephem.earth_radius / (siteGem.elevation + ephem.earth_radius))
    siteGem.horizon = hza
    
    # Convert float of the decimal degrees RA/Dec to floating radians
    raTargetrad = math.radians(args.ra)
    decTargetrad = math.radians(args.dec)
    
    # Set target as fixed body and compute for location
    target = ephem.FixedBody()
    target._ra = raTargetrad
    target._dec = decTargetrad
    target.compute(siteGem)
    
    altTarget = math.degrees(target.alt)
    azTarget =  math.degrees(target.az)

    print(target.ra)
    print(target._ra)
    print(target.dec)
    print(target._dec)

    print(altTarget)
    print(azTarget)    
    
    return


def create_parser():
    """ create_parser() doc
    """
    parser = argparse.ArgumentParser(description="",
        epilog='Version: ' + __version__)

    parser.add_argument('filename', type=str,
        help="filename of image ex: 201220-184817.jpg")
    parser.add_argument('ra', type=float,
        help="ra coordinate as decimal degrees (NOT HR:MIN:SEC) value")
    parser.add_argument('dec', type=float,
        help="dec coordinate as decimal degrees value")
    parser.add_argument('-d', '--debug', action='store_true', dest='debug',
        default=False, help='(optional) Print additional debug lines')

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)


