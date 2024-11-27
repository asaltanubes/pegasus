from astros import AstroList

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
def save_positions(positions: list[AstroList]):
    """ 
    Saves all data regarding the Astros in a file for every time step
    calculated (an AstroList)
    """
    # Me gustaria que los datos se guarden en una carpeta
    for astro in positions[0].get_all_astros(): # Para cada planeta
        file_name = f"./output_data/{astro.name}.dat"
        with open(file_name,'w') as data_file:
            data_file.write(f"{astro.name},  {astro.mass} \n")
            for astrolist in positions:
                data_file.write(','.join([str(x) for x in astro.position]))
                # data_file.write(astro.velocity +',')
                # data_file.write(astro.potential_energy +',')
                data_file.write('\n')
        data_file.close()




