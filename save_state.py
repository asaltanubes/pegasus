from astros import AstroList

# 
"""
# nombres sol, tierra, luna, ...

sol masa, tierra masa, luna masa, ...
tiempo, solx, soly, solz, solvx, solf
"""

file = 'positions.output'
points = AstroList()


"""
for i in range(len(points[0].get_astros()))
with open file
for astrolist
astro = astrolist.get_astros[i]
file
"""

def save_points(points: list[AstroList]):
    """ 
    Saves all data regarding the Astros in a file for every time step
    calculated (an AstroList)
    """
    for i in range(len(points[0].get_astros())):
        astrolist = points[0]
        astro = AstroList.get_astros[i]
        with open(f"{astrolist()astro.name}.dat",'w') as data_file:
            data_file.write(astrolist.get_astros()[i].mass + '\n')
            for astrolist in points:
                astro = astrolist.get_astros()[i]
                data_file.write(astro.position +',')
                # data_file.write(astro.velocity +',')
                # data_file.write(astro.potential_energy +',')
                data_file.write('\n')






# import numpy as np

# a = np.array[(1,2,3)],
# with open('ejemplo.txt', 'w') as file:
#     file.write(a + '\n')
#     file.write(a + '\n')

# print(file.read())

