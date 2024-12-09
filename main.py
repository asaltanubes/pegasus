from astros import *
from verlet import *
from file_io import *
import matplotlib.pyplot as plt
import numpy as np
from animation import create_animation
from save_state import save_positions
from eclipse_search import *
from moon_phase import get_moon_phase
"""
- Añadir progreso a la ejecución del programa ?
- borrar diff_eq, initial_test, notebook
- borrar mucho codigo comentado por ahi
- update_forces sirve para algo?
- update_state necesita forces y potential?
- use velocity read se está teniendo en cuenta?
- plot sin ejes con fondo negro para el power point
- ¿¿Guardar input: initial_conditions y simulation_parameters??

Por alguna razón que escapa completamente a mi entendimiento, Junquera hace esto para la Luna cunado está leyendo el file de los astros:

    if name_astro == "Moon":
        speed_astro = np.sqrt( np.longdouble(G) * mass_sun / np.longdouble(149597871.0e3)) + np.sqrt( np.longdouble(G) * np.longdouble(5.9724e24) / np.longdouble(384400.0e3))
        velocity_astro = np.array([0.0,speed_astro,0.0],dtype=np.longdouble)
        astro.set_velocity( velocity_astro )

"""


"""
This script runs a simulation for the system given in initial_conditions.ini.
It propagates the state of the astronomical system over the given Delta_time*Number_steps 
specified in the simulation_parameters. Afterwards, it saves several graphs and displays results.
"""


def main():
    """
    Description
    """

    # Read the initial conditions
    astrolist = load_initial_condition("initial_conditions.ini")

    # Read and load the simulation parameters
    params = load_configuration("simulation_parameters.conf")

    # Generate the Velocity Verlet integration method implementation
    verlet = Verlet(params.delta_time)

    final_time = params.delta_time * params.number_steps 

    # Display initial conditions and parameters
    print(f"Initial conditions \n {astrolist}")
    print()
    print(f"Parameters: \n{params}")
    print(repr(astrolist.time))

    # earth = astrolist.get_astro_by_name("earth")
    # theta0_earth = np.arctan2(earth.position[1], earth.position[0])

    # All astrolist are stored
    astrolist_states = np.array([])
    step = 0

    # For the functioning of the eclipse search
    last_time_eclipse = False

    # Propagate the astrolist state for given final_state
    while astrolist.time < final_time:
        print(f"Simulation is {astrolist.time.item()/final_time*100:.3f}% complete!", end="\r")
        astrolist = verlet.advance_time(astrolist, params.delta_time+astrolist.time)
        astrolist_states = np.append(astrolist_states, astrolist.copy())
        
        #  Check for eclipses over the time of simulation
        last_time_eclipse = eclipse_check(astrolist, last_time_eclipse)

        # positions.append([i.position for i in astrolist.get_free_astros()])
        # com.append(astrolist.center_of_mass)
        # kinetic_energy.append(astrolist.kinetic_energy())
        # potential.append(astrolist.potential)
        # astro_positions.append(astrolist.copy())  # Rulo test

        # angular_momentum.append(astrolist.angular_momentum())

        # times.append(astrolist.time)
        # theta_earth = np.arctan2(earth.position[1], earth.position[0])
        # if np.abs(theta0_earth-theta_earth) < np.pi/(360*12):
        #     print(f"New year!: {astrolist.time/(3600*24)} day")
        step += 1
    print("                                           ", end = "\r")
    print("Simulation complete!")

    # Saves all positions in different files for each astro
    save_positions(astrolist_states) 
    times = np.array([astrolist.time for astrolist in astrolist_states])
    
    angular_momentum = np.array([astrolist.angular_momentum() for astrolist in astrolist_states])
    x_angular_momentum = np.array([a[0] for a in angular_momentum])
    y_angular_momentum = np.array([a[1] for a in angular_momentum])
    z_angular_momentum = np.array([a[2] for a in angular_momentum])
    
    print(f"Max of the angular momentum x component: {np.max(x_angular_momentum)}, minumum of the angular momentum x component: {np.min(x_angular_momentum)}")
    print(f"Max of the angular momentum y component: {np.max(y_angular_momentum)}, minumum of the angular momentum y component: {np.min(y_angular_momentum)}")
    print(f"Variation of the angular momentum z component: {(np.max(z_angular_momentum)-np.min(z_angular_momentum))/(np.mean(z_angular_momentum))}")
    
    plt.plot(times, (z_angular_momentum-np.mean(z_angular_momentum))/np.mean(z_angular_momentum))
    plt.title('Relative deviation of\n the z component of total Angular momentum')
    plt.savefig('output_data/angular_momentum.svg')
    plt.show()
    
    angular_momentum = None
    x_angular_momentum = None
    y_angular_momentum = None
    z_angular_momentum = None

    


    total_energy = np.array([astrolist.potential for astrolist in astrolist_states]) + np.array([astrolist.kinetic_energy() for astrolist in astrolist_states])
    
    print(f"Variation of the energy: {(np.max(total_energy)-np.min(total_energy))/(np.mean(total_energy))}")
    plt.plot(times, (total_energy-np.mean(total_energy))/np.mean(total_energy))
    plt.title('Relative deviation of Energy')
    plt.savefig('output_data/energy_conservation.svg')
    plt.show()
    
    total_energy = None

    positions = [[i.position for i in astrolist.get_all_astros()] for astrolist in astrolist_states]
    com = [astrolist.center_of_mass for astrolist in astrolist_states]
    # with open("positions.output", "wt") as file:
    #     file.write("\n".join([", ".join([str(j) for j in i]) for i in positions]))
    for i in range(len(astrolist_states[0].get_free_astros())):
        plt.plot([j[i][0] for j in positions], [j[i][1] for j in positions])
    plt.plot([i[0] for i in com], [i[1] for i in com], marker="o")
    plt.gca().set_aspect('equal')
    plt.savefig("output_data/position_output.svg")
    plt.show()

    plt.plot([i[0] for i in com], [i[1] for i in com])
    plt.title("COM")
    plt.savefig("output_data/COM.svg")
    plt.show()
    positions = None
    com = None
    

    # Check the moon phase on New Years Eve

    get_moon_phase(astrolist_states[-1],"output_data/moon_phase")


    create_animation(astrolist_states[::params.animation_step], "output_data/animation")


if __name__ == "__main__":
    main()
