"""
The following module implements a function that will enable the tracking
and searching of solar eclipses. 
"""
from astros import AstroList, Astro
import numpy as np


def eclipse_check(astrolist: AstroList):
    """
    Checks if the current state of the system formed by sun, earth, and moon,
    is in an eclipse like configuration.
    The moon is eclipsed by the earth or the earth by the moon.
    """
    sun = astrolist.get_astro_by_name('sun')
    earth = astrolist.get_astro_by_name('earth')
    moon = astrolist.get_astro_by_name('moon')

    sun_position = sun.position
    earth_position = earth.position
    moon_position = moon.position

    # Define r1 as the distance from sun to earth and r2 as the distance from sun to the moon.
    r1 = earth_position - sun_position
    r2 = moon_position - sun_position
    r1_norm, r2_norm = np.linalg.norm(np.vstack([r1, r2]),axis = 1) 

    theta = np.arccos(np.linalg.norm(np.dot(r1,r2))/(r1_norm*r2_norm))
    alpha = np.arctan(earth.radius/r1_norm)
    beta = np.arctan(moon.radius/r2_norm)
    if (alpha+beta)>theta:
        print(f'Eclipse! on {astrolist.time}')

    # Create a function that transforms seconds to years, day, hour!!


def search_eclipse(astrolist):
    """
    Given an AstroList description of the system, this function runs 
    the simulation until an eclipse is found. Updating the state and
    checking if it is the case.
    More efficcient way? Could we calculate the eclipses  date?

    """
    #  ...
    date = astrolist.time
    print(f'Eclipse due {date}')

    

