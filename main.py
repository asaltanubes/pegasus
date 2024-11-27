from astros import *
from verlet import *
from file_io import *
import matplotlib.pyplot as plt
import numpy as np
from save_state import save_positions
"""
- Borrar todo lo que no sea útil y simplificar cosas (muchas cosas)
- Para los mismos parámetros de simulación, nuestro código es al menos 2 segundos más lento que el suyo
- Printear de mejor manera las initial conditions
- Añadir progreso a la ejecución del programa ?
-

Cosas que no tenemos con respecto a Junquera:
    - Astro.filename
    - Astro.acceleration
    - Astro positions in polars or center of mass
    - Getters / Setters / Printers
    - AstroList.add_astro / remove_astro


Por alguna razón que escapa completamente a mi entendimiento, Junquera hace esto para la Luna cunado está leyendo el file de los astros:

    if name_astro == "Moon":
        speed_astro = np.sqrt( np.longdouble(G) * mass_sun / np.longdouble(149597871.0e3)) + np.sqrt( np.longdouble(G) * np.longdouble(5.9724e24) / np.longdouble(384400.0e3))
        velocity_astro = np.array([0.0,speed_astro,0.0],dtype=np.longdouble)
        astro.set_velocity( velocity_astro )

"""


def main():
    astrolist = load_initial_condition("initial_conditions.ini")

    params = load_configuration("simulation_parameters.conf")

    verlet = Verlet(params.delta_time)

    final_time = params.delta_time * params.number_steps

    positions = []
    potential = []
    kinetic_energy=[]
    angular_momentum = []
    com = []
    times = []
    astro_positions = [] # Rulo test

    print(f"Initial conditions \n {astrolist}")
    print()
    print(f"Parameters: \n{params}")

    earth = astrolist.get_astro_by_name("earth")
    theta0_earth = np.arctan2(earth.position[1], earth.position[0])

    while astrolist.time < final_time:
        astrolist = verlet.advance_time(astrolist, params.delta_time+astrolist.time)
        positions.append([i.position for i in astrolist.get_free_astros()])
        com.append(astrolist.center_of_mass)
        kinetic_energy.append(astrolist.kinetic_energy())
        potential.append(astrolist.potential)
        astro_positions.append(astrolist)  # Rulo test

        angular_momentum.append(astrolist.angular_momentum())

        times.append(astrolist.time)
        theta_earth = np.arctan2(earth.position[1], earth.position[0])
        if np.abs(theta0_earth-theta_earth) < np.pi/(360*12):
            print(f"New year!: {astrolist.time/(3600*24)} day")

    save_positions(astro_positions) # Saves all positions in different files for each astro
    
    potential = np.array(potential)
    kinetic_energy = np.array(kinetic_energy)
    total_energy = potential+kinetic_energy
    x_angular_momentum = [a[0] for a in angular_momentum]
    y_angular_momentum = [a[1] for a in angular_momentum]
    z_angular_momentum = [a[2] for a in angular_momentum]

    print(f"Variation of the energy: {(np.max(total_energy)-np.min(total_energy))/(np.mean(total_energy))}")
    print(f"Max of the angular momentum x component: {np.max(x_angular_momentum)}, minumum of the angular momentum x component: {np.min(x_angular_momentum)}")
    print(f"Max of the angular momentum y component: {np.max(y_angular_momentum)}, minumum of the angular momentum y component: {np.min(y_angular_momentum)}")
    print(f"Variation of the angular momentum z component: {(np.max(z_angular_momentum)-np.min(z_angular_momentum))/(np.mean(z_angular_momentum))}")

    with open("positions.output", "wt") as file:
        file.write("\n".join([", ".join([str(j) for j in i]) for i in positions]))
    for i in range(len(astrolist.get_free_astros())):
        plt.plot([j[i][0] for j in positions], [j[i][1] for j in positions])
    plt.plot(0,0,'or')
    plt.gca().set_aspect('equal')
    plt.show()

    plt.plot([i[0] for i in com], [i[1] for i in com])
    plt.show()

    plt.plot(times, total_energy)
    plt.title('Total Energy')
    plt.show()
    plt.plot(times, z_angular_momentum)
    plt.title('Angular momentum')
    plt.show()



if __name__ == "__main__":
    main()
