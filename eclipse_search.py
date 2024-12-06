"""
The following module implements a function that will enable the tracking
and searching of solar eclipses. 
"""
from astros import AstroList, Astro
import numpy as np


def eclipse_check(astrolist: AstroList):
    """
    INPUT: Given an Astrolist. Podría ser metodo de Astrolist
    Checks if the current state of the system formed by sun, earth, and moon,
    is in an eclipse like configuration.
    The moon is eclipsed by the earth or the earth by the moon.
    """
    r_earth = 6378000 # m
    r_moon = 1737500 # m

    sun = astrolist.get_astro_by_name('sun')
    earth = astrolist.get_astro_by_name('earth')
    moon = astrolist.get_astro_by_name('moon')

    sun_position = sun.position
    earth_position = earth.position
    moon_position = moon.position

    # Define r1 as the distance from sun to earth and r2 as the distance from sun to the moon.
    r1 = np.subtract(earth_position, sun_position)
    r2 = np.subtract(moon_position, sun_position)
    r1_norm, r2_norm = np.linalg.norm(np.vstack([r1, r2]),axis = 1) 

    theta = np.arccos(np.linalg.norm(np.divide(np.dot(r1,r2),(r1_norm*r2_norm))))
    alpha = np.arctan(np.divide(r_earth,r1_norm))
    beta = np.arctan(np.divide(r_moon,r2_norm))
    if (alpha+beta) > theta:
        print(f'Eclipse! on {astrolist.time}')

    # Create a function that transforms seconds to years, day, hour!!


def search_eclipse(sun_positions: list, earth_positions: list, moon_positions: list, time):
    """
    INPUT: lista de posiciones
    Argumentos? un txt, o tres arrays con las posiciones, da igual
    Given a set of positions (sun,earth,moon), this function checks if 
    any is compatibles with an eclipse.
    Returns -index- for which we find an eclipse. 
    More efficcient method than the first.
    1 year = (365 days, 5 hours, 49 minutes, 1.1 seconds)
    """
    r_earth = 6378000 # m
    r_moon = 1737500 # m

    r1 = np.subtract(earth_positions, sun_positions)
    r2 = np.subtract(moon_positions, sun_positions)

    r1_norm, r2_norm = np.linalg.norm(r1,axis = 1), np.linalg.norm(r2,axis = 1) 
    theta = np.arccos(np.linalg.norm(np.divide(np.dot(r1,r2)),(r1_norm*r2_norm)))
    alpha = np.arctan(np.divide(r_earth,r1_norm))
    beta = np.arctan(np.divide(r_moon,r2_norm))
    value = np.subtract(np.sum(alpha,beta),theta)

    eclipses_time = []

    # return[i for theta[i] in theta if  theta[i]<(alpha[i]+beta[i])] como lo hago así?
    # Los que sí son eclipses, guardo su indice
    for i, t in enumerate(value):
        if t<0:
            eclipses_time.append(time[i])
    return(eclipses_time)
            
    # Si ponemos la fecha de inicio como argumento, podria dar como resultado fechas
    # return(date_0+i*dt) 










def seconds_to_years(time_s: float):
    """
    Given a number of seconds, it translates the amount to Years and Days
    """
    y = 365.24 # days/y
    years = time_s//(3600*24*y)
    rest_year = time_s/(3600*24*y)-years
    days = rest_year*y
    return(f"{years} years, {days} days")


a = (((365.24*2)+180)*24+8)*3600
print(seconds_to_years(a))
    

    

