# -*- coding: utf-8 -*-
"""
The following script studies Moon phases, their nomenclature
and exact representation given a certain position between the 
Sun, Moon and Earth.

Created on Wed Nov 27 2024

@author: raul
"""
import numpy as np
import matplotlib.pyplot as plt
from astros import *



def get_moon_phase(system: AstroList):
    """
    Prints an exact simulation of the moon phase and its English name given
    an Astrolist. Will let the user know the moon phase in any given point of time.
    Args:
        system (Astrolist): Astrolist including the Sun, Earth and Moon, and their respective 
                            positions and velocities.
    """
    # Get the astros
    earth = system.get_astro_by_name('earth')
    moon = system.get_astro_by_name('moon')
    
    # Get and calculate needed positioning vectors
    r_earth = earth.position 
    r_moon = moon.position
    r_e_m = r_earth -r_moon

    # Calculate the angle fromed by the Moon-Earth and Sun-Earth lines. Using scalar product.
    u, v = r_e_m, r_earth
    theta = np.arccos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))

    # Since np.arccos() is only defined from [0,pi] the sign helps distinguish in [0,2pi]
    sign = np.sign(np.dot(r_e_m, earth.velocity))


    phases = ['New Moon', 'Wanning Crescent', 
            'Last Quarter', 'Wanning Gibous', 
            'Full Moon', 'Waxing Gibbous', 
            'First Quarter', 'Waxing Crescent']

    rad = np.pi/180

    #  Assign the correct Moon Phase name, given the angle theta 

    if theta <= 10*rad and theta > 0:
        phase = phases[0]
    elif 10*rad<theta<=80*rad and sign <0:
        phase = phases[1]
    elif 80*rad<theta<=100*rad and sign <0:
        phase = phases[2]
    elif 100*rad<theta<=170*rad and sign <0:
        phase = phases[3]
    elif 170*rad<theta<=180*rad:
        phase = phases[4]
    elif 100*rad<theta<=170*rad and sign >0:
        phase = phases[5]
    elif 80*rad<theta<=100*rad and sign >0:
        phase = phases[6]
    elif 10*rad<theta<=80*rad and sign >0:
        phase = phases[7]
    # print(phase)


    # Changes nomenclature of theta and defines linspaces in order to plot the phase 
                
    x = theta
    R = 1  # The radius of the figures to plot
    theta_ax = np.linspace(0,2*np.pi,360)
    phi = np.linspace(0,np.pi,500)
    r = np.linspace(-np.sqrt(R),np.sqrt(R),360)

    # Do the plot, black background, dark gray circle for the moon
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor((0.07,0.07,0.07))
    plt.fill(R*np.cos(theta_ax), R*np.sin(theta_ax), c=(0.1,0.1,0.1))

    # Plot visible part of the moon, light gray. Inlcude the moon phase on the title
    x = np.append(R*np.sin(phi), np.cos(x)*np.sqrt(R**2-r**2)) * (sign if not np.isclose(sign, 0) else 1)
    y = np.append(R*np.cos(phi),r)
    plt.fill(x,y, 'gray')
    plt.title(f'Moon Phase: {phase}')
    plt.show()

    # TESTING
    # theta_vec = np.pi/180*np.array([5,40,90,120,180,200,270,290,355])
    # sign
    # for theta in theta_vec: