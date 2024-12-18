# -*- coding: utf-8 -*-
"""
This script allows to create an initial position and velocity file
making it faster to get different initial conditions. For running the main program 
it will only be required to include the masses. 

Usefull to extract data from Ephemeris downloaded from Horizon System (NASA): 

https://ssd.jpl.nasa.gov/horizons/app.html#/ 


---PART OF AN ATTEMP TO AUTOMATIZE THE MASS LECTURE---
Is included, this idea had to be abandoned since the format of the downloaded 
files was not the same: using different exponent format, sometimes in diferent units...



Created on Wed Nov 6 2024

@author: raul
"""
import numpy as np




def read_files(number_of_files: int):
    """
    Reads a number_of files with name format 'horizons_results ({i}).txt' located in the folder 
    /data_tables_reader/website_2/web_data
    Gets the name of the Astros, and their initial velocity and masses, and generates a txt file with 
    arranged data.

    IMPORTANT:
    Horizon System distances and velocities are in Km units, thus this function converts them to SI (m and m/s)

    Args:
        number_of_files (int):  
    """

    # Route of the file where the collected data will be written
    output_file_name = './data_tables_reader/website_2/initial_conditions.ini'

    with open(output_file_name, 'w')  as file:

        file.truncate(0)

        #  Write the header with legend
        file.write('# Name, x, y, z, vx, vy, vz (DATE: on last line)\n')
        
    # Open each astro file 
    for i in range(0,number_of_files):

        file_name:str = f'./data_tables_reader/website_2/web_data/horizons_results ({i}).txt'

        with open(file_name) as f:

            lines = f.readlines() 
            # cond = True # To get the mass 
            for n, line in enumerate(lines): 

                # Search for the Body name    
                if ' '.join(line.split(' ')[0:3]).strip().lower() == 'target body name:':

                    # Save name
                    astro_name = line.split(' ')[3].strip().lower()

                # Search for the previous line to positions 
                if ' '.join(line.split(' ')).strip().lower() == '$$soe':

                    # Save number of line that will be used as reference
                    marker_position = n 

                # ---PART OF AN ATTEMP TO AUTOMATIZE THE MASS LECTURE---

                # if 'mass' in line.lower() and cond == True:
                #     cond = False
                #     marker_mass = n
                #     print(line)
                #     try:
                #         index_mass = line.lower().split('\t').index('mass')
                #     except: 
                #         index_mass = line.lower().split('\t').index('mass,')
                #         pass
                #     print(index_mass)
                #     # index_mass = lines[n].split('\t').index('mass')
                #     # mass_line = lines[n].split(' ')[index_mass, lines[marker_mass].split(' ').index()+2]
                #     # print(mass_line)

            # Save date, positions and velocities lines
            date_line = lines[marker_position+1]
            position_line = lines[marker_position+2].split('=')
            velocity_line = lines[marker_position+3].split('=')
            # mass_line = lines[marker_mass].split(' ').index()

            # Select each piece of the velocity-position vectors
            position = [position_line[1].strip().split(' ')[0].strip(),
                        position_line[2].strip().split(' ')[0].strip(),
                        position_line[3].strip().split('\n')[0].strip()]
            
            velocity = [velocity_line[1].strip().split(' ')[0].strip(),
                    velocity_line[2].strip().split(' ')[0].strip(),
                    velocity_line[3].strip().split('\n')[0].strip()]
            f.close()

        # ---FOR TESTING---
        # print(date_line)
        # print(astro_name)
        # print(position) 
        # print(velocity)
        


        # Save the data line for this astro
        # We multiply by 1000 to make km to m
        # 'a' stands for append
        with open(output_file_name, 'a')  as file:

            file.write(f'{astro_name},\t {',\t'.join([str(1000*eval(i)) for i in position])},\t{',\t'.join([str(1000*eval(i)) for i in velocity])},\n')

    # Finally, saves the date of the position and velocity data. Without it, data would be worthless
    with open(output_file_name, 'a')  as file:

        file.write('#\t DATE: '+ date_line + '\n')
    


# Run for 10 files
# Having to check this number manually helps to makes sure you don't mess up 
read_files(10)