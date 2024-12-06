"""
Simulation of the Moon's Phase seen from the Earth
"""
import numpy as np
import matplotlib.pyplot as plt
from astros import *



def get_moon_phase(system: AstroList):

    earth = system.get_astro_by_name('earth')
    moon = system.get_astro_by_name('moon')

    r_earth = earth.position
    r_moon = moon.position
    r_e_m = r_earth -r_moon
    # Calculate the angle fromed by the Moon-Earth and Sun-Earth lines. 
    theta = np.asin(np.cross(r_e_m, r_earth)/np.linalg.norm(r_e_m)/np.linalg.norm(r_earth))

    while theta<0:
        theta = theta+2*np.pi

    phases = ['New Moon', 'Wanning Crescent', 
              'Last Quarter', 'Wanning Gibous', 
              'Full Moon', 'Waxing Gibbous', 
              'First Quarter', 'Waxing Crescent']
    rad = np.pi/180
    if theta <= 10*rad or theta > 350*rad:
        phase = [0]
    elif 10*rad<theta<=35*rad:
        phase = [1]
    elif 35*rad<theta<=55*rad:
        phase = [2]
    elif 55*rad<theta<=170*rad:
        phase = [3]
    elif 170*rad<theta<=190*rad:
        phase = [4]
    elif 190*rad<theta<=260*rad:
        phase = [5]
    elif 260*rad<theta<=280*rad:
        phase = [6]
    elif 280*rad<theta<=350*rad:
        phase = [7]
               
    # Do a plot now

