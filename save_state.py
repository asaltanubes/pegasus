from astros import AstroList
import os

#
"""
# nombres sol, tierra, luna, ...
sol masa, tierra masa, luna masa, ...
tiempo, solx, soly, solz, solvx, solf
"""


"""
for i in range(len(positions[0].get_astros()))
with open file
for astrolist
astro = astrolist.get_astros[i]
file
"""

# a partir de una lista de objetos AstroList
def save_positions(list_astros: list[AstroList]):
    """
    Saves position data for celestial bodies to data files.

    Takes a list of AstroList objects containing position information for multiple celestial bodies
    and saves the data to individual .dat files in the output_data directory. Each file contains
    the body's name, mass, and position coordinates over time.

    Args:
        positions: A list of AstroList objects containing position and properties of celestial bodies
    """
    # Me gustaria que los datos se guarden en una carpeta
    for astro in list_astros[0].get_all_astros(): # Para cada planeta
        file_name = f"output_data/astro_data/{astro.name}.dat"
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name,'w') as data_file:
            data_file.write(f"{astro.name},  {astro.mass} \n")
            for astrolist in list_astros:
                data_file.write(','.join([str(x) for x in astro.position] +
                                         [str(x) for x in astro.pos_com] +
                                         [str(x) for x in astro.velocity] + 
                                         [str(x) for x in astro.force] + 
                                         [str(astro.potential)]))
                data_file.write('\n')
