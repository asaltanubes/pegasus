# -*- coding: utf-8 -*-
"""
Script dedicated to saving the positions for all astros in the 
steps of time of the simulation. As well as the inital parameters and positions

Created on Wed Dic 4 2024

@author: raul, gustavo
"""
 
from astros import AstroList
import os
from shutil import copyfile



# a partir de una lista de objetos AstroList
def save_astros(list_astros: list[AstroList]):
    """
    Saves position data for celestial bodies to data files. Also saves initial parameters.

    Takes a list of AstroList objects containing position information for multiple celestial bodies
    and saves the data to individual .dat files in the output_data directory. Each file contains
    the body's name, mass, and position coordinates over time.

    Args:
        positions: A list of AstroList objects containing position and properties of celestial bodies
    """
    
    # Saves the initial parameters and initial conditions for future reference

    copyfile("simulation_parameters.conf", "output_data/simulation_parameters.conf")
    copyfile("initial_conditions.ini", "output_data/initial_conditions.ini")

    # Save the data for every planet in a different file, all in the same folder
    for i in range(len(list_astros[0].get_all_astros())): 

        astro = list_astros[0].get_all_astros()[i]

        file_name = f"output_data/astro_data/{astro.name}.dat"

        # In case the file_name 
        os.makedirs(os.path.dirname(file_name), exist_ok=True)

        with open(file_name,'w') as data_file:

            data_file.write(f"{astro.name},  {astro.mass} \n")

            for astrolist in list_astros:
                astro = astrolist.get_all_astros()[i]
                data_file.write(','.join([str(x) for x in astro.position] +
                                        [str(x) for x in astro.pos_com] +
                                        [str(x) for x in astro.velocity] + 
                                        [str(x) for x in astro.force] + 
                                        [str(astro.potential)]))
                data_file.write('\n')
