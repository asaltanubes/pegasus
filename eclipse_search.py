# -*- coding: utf-8 -*-
"""
The following script implements a function in order to study eclipses.
This way it will be possible to predict Solar and Moon Eclipses, discriminating 
both types and getting the exact week and day of the event.

Created on Wed Nov 20 2024

@author: raul
"""
from astros import AstroList, Astro
import numpy as np



def eclipse_check(astrolist: AstroList, last_time_eclipse: bool) -> bool:
    """
    Checks if the configuration of the Sun, Moon and Earth is compatible
    with an eclipse, comparing the shadow of both bodies with the angular separation
    in between them. 

    Args:
        astrolist (Astrolist): Astrolist including the Sun, Earth and Moon, and their respective 
                               positions and velocities.
        last_time_eclipse (bool): Boolean showing if the last checked Astrolist had an elcipse. Used to avoid
                                  pointing out the same eclipse several times.

    Returns:
        Boolean showing if an elcipse was found, to be used as last_time_eclipse
    """
    # Rasius of sun and moon, used to calculate their "shadow"
    r_earth = 6378000 # m
    r_moon = 1737500 # m

    # Get the 3 bodies of interest and their positions
    sun = astrolist.get_astro_by_name('sun')
    earth = astrolist.get_astro_by_name('earth')
    moon = astrolist.get_astro_by_name('moon')

    sun_position = sun.position
    earth_position = earth.position
    moon_position = moon.position

    # Define r1 as the sun-earth distance and r2 as the sun-moon distance, and their norms
    r1 = np.subtract(earth_position, sun_position)
    r2 = np.subtract(moon_position, sun_position)
    r1_norm, r2_norm = np.linalg.norm(np.vstack([r1, r2]),axis = 1) 

    # Calculate necessary angles, theta angle between moon and earth, alpha earth-radius angle
    #   and beta moon-radius angle
    theta = np.arccos(np.linalg.norm(np.divide(np.dot(r1,r2),(r1_norm*r2_norm))))
    alpha = np.arctan(np.divide(r_earth,r1_norm))
    beta = np.arctan(np.divide(r_moon,r2_norm))

    # Set the condition for an eclipse
    if (alpha+beta) > theta:
        # Check if another eclipse was just found
        if not last_time_eclipse: 
            # Check if eclipse was a Moon or Earth Eclipse and print date, .item() transforms to a handle number   
            print(f"{'Sun' if r1_norm>r2_norm else 'Moon'} Eclipse! on {seconds_to_years(astrolist.time.item())} (since sim. start)")

        last_time_eclipse = True 

    else:
        last_time_eclipse = False

    return(last_time_eclipse)
        

def seconds_to_years(time_s: float) -> str:
    """
    User-friendly function to display data. Transforms time from 
    seconds to a more readable format years, week, days.
    
    Args:
        time_s (float): Amount of time as a number of seconds.

    Returns (str):  
         A formated string showing the amount of seconds as 
        years, weeks, days.  
    
    """

    y = 365.24 # days/y
    years = time_s//(3600*24*y)
    rest_year = (time_s/(3600*24*y)-years)
    weeks = rest_year*y//7
    days = (rest_year*y/7 - weeks)*7
    return(f"year {years}, week {weeks}, day {round(days)}")



# def search_eclipse(sun_positions: list, earth_positions: list, moon_positions: list, time):
#     """
#     Poject of similar function to be applied to a list of positions instead of just
#     one Astrolist. More efficient, but not refined
#     """
#     r_earth = 6378000 # m
#     r_moon = 1737500 # m

#     r1 = np.subtract(earth_positions, sun_positions)
#     r2 = np.subtract(moon_positions, sun_positions)

#     r1_norm, r2_norm = np.linalg.norm(r1,axis = 1), np.linalg.norm(r2,axis = 1) 
#     theta = np.arccos(np.linalg.norm(np.divide(np.dot(r1,r2)),(r1_norm*r2_norm)))
#     alpha = np.arctan(np.divide(r_earth,r1_norm))
#     beta = np.arctan(np.divide(r_moon,r2_norm))
#     value = np.subtract(np.sum(alpha,beta),theta)

#     eclipses_time = []

#     # return[i for theta[i] in theta if  theta[i]<(alpha[i]+beta[i])] como lo hago así?
#     # Los que sí son eclipses, guardo su indice
#     for i, t in enumerate(value):
#         if t<0:
#             eclipses_time.append(time[i])
#     return(eclipses_time)
            
#     # Si ponemos la fecha de inicio como argumento, podria dar como resultado fechas
#     # return(date_0+i*dt) 


# TEST for second_to_years():

# a = (((365.24*2))+7*5+3)*24*3600
# print(seconds_to_years(a))
    

    

