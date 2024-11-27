"""
This module will get two .txt files with a copy from the position of astros 
given by the following website:
  http://cosinekitty.com/solar_system.html
and write a new txt file including the name, position and velocities of this astros.
Valocities will be computed using differences of the position.
"""

import numpy as np

def rewrite_table_web(og_file_name: str):
    with open(og_file_name, 'rt') as file:
        lineas = []
        for n, line in enumerate(file.readlines()):
            if line.strip() == "":
                continue
            if line.strip()[0] == '#':
                continue
            lineas.append(line.lower().strip())
            # print(line)
            # lineas.append(line.split("\n")[0])
        # print(lineas)
        file.close()
    file2_name = og_file_name.split('.')[0].strip()+'_v2.txt'
    with open(file2_name, 'w') as file2:
        file2.write('#' +'\t'.join(lineas[0].split('\t')[0:4])+"\n")
        for i in range(0,4):
            file2.write(lineas[1+4*i]+"\t"+'\t'.join(lineas[2+4*i].split("\t")[0:3])+ "\n")
        # Divido el loop porque la Tierra tiene 2 lineas menos de datos
        for i in range(3,14):
            file2.write(lineas[3+4*i]+"\t"+'\t'.join(lineas[4+4*i].split("\t")[0:3])+ "\n")
    return(file2_name)



def create_data_file_from_website(file_name1: str, file_name2: str, delta_time: float):
    astros = []
    positions_1 = np.array([])
    positions_2 = np.array([])
    with open (file_name1, "rt") as f:
        for n, line in enumerate(f.readlines()):
            if line.strip() == "":
                continue
            if line.strip()[0] == '#':
                continue
            astro = [i.strip().lower() for i in line.split("\t") if i.strip() != ""]
            astros.append(astro[0].lower())
            positions_1 = np.append(positions_1, np.array([float(i) for i in astro[1:4]], dtype=np.longdouble))
            # print(np.array([float(i) for i in astro[1:3]], dtype=np.longdouble))
            # print(positions_1)
    with open (file_name2, "rt") as f:
        for n, line in enumerate(f.readlines()):
            if line.strip() == "":
                continue
            if line.strip()[0] == '#':
                continue
            astro = [i.strip().lower() for i in line.split("\t") if i.strip() != ""]
            if astro[0] not in astros:
                print(f'El error le da {astro[0]}; {astros}')
                raise('The given files contain different astros')
            positions_2 = np.append(positions_2, np.array([i for i in astro[1:4]], dtype=np.longdouble))
    velocity = (positions_1-positions_2)/delta_time
    # print(len(astros))
    with open ("./data_tables_reader/website_1/Initial_position_velocity.txt", "w") as file:
        file.write("# Name, x, y, z, vx, vy, vz \n")
        for i, astro in enumerate(astros):
            # print(i, astro)
            file.write(astros[i]+ "\t"+"\t".join([str(i) for i in positions_1[3*i:(3*i+3)]])+"\t"+
                       "\t".join([str(i) for i in velocity[3*i:(3*i+3)]])+"\n")

    file.close()  

     

def position_velocity_file(file1:str, file2:str, dt:float):
    """
    Given two tables form the website, directly copied on two .txt files with names
    file1 and file2, taken in two points of time separated dt (seg).
    This function rewrites both files arranging the data by planets and inlcuding only 
    and then generates a single .txt file named "Initial_position_velocity.txt"
    including the position (UA) and and velocity (UA/seg).
    A much cleaner file, that can be used for later on initiliazing the program
    """
    new_file1 = rewrite_table_web(file1)
    new_file2 = rewrite_table_web(file2)
    create_data_file_from_website(new_file1, new_file2, dt)


# EJEMPLO DE USO
position_velocity_file("./data_tables_reader/website_1/posiciones1.txt","./data_tables_reader/website_1/posiciones2.txt",1)

        



            




        

