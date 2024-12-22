# -*- coding: utf-8 -*-
"""
Pegasus Software allows you to run a Astronomical Body System simulation for the
system given in initial_conditions.ini, It propagates the state of the  system
over the given Delta_time*Number_steps specified in the simulation_parameters. 
It saves several graphs and displays results, such as:

- Angular momentum variation    
- Energy conservation
- Position of each astronomical body
- Center of Mass (COM) trajectory
- Eclipses' dates
- Moon Phases

   *    ✧    *    ·    ⋆    *    ✧    *     ·     *
 ✦   ____       *                    ✧           *
*   |  _ |_____  __ _  __ _ ___ _   _ ___    ⋆
  * | |_) / _ |/ __` |/__` / __| | | / __|  *   ·
✧   |  __/  __/ (_| | (_| |__ | |_| |__ |    *
 *  |_|   |___|___, ||__,_|___/|__,_|___/  ✧    *
  *            |___/     *    ·     *    ⋆
    *    ·     *    ✧    *    ·     *    ✧     *

Created on Wed Oct 9 2024

@author: gustavo, oscar
"""

import matplotlib.pyplot as plt
import numpy as np

from astros import *
from verlet import *
from file_io import *
from animation import create_animation
from save_state import save_astros
from eclipse_search import *
from moon_phase import get_moon_phase
from kepler import kepler


def main():
    """
    Main function, runs the simulation for the given initial data and parameters, 
    propagates the state of the system over time. Prints initial data and parameters, runs simulation 
    while showing a progress bar. Finally, saves the positions in the output_data folder.
    Pots and saves grpahs for angular momentum, energy and position over time.

    Additionally, searches for eclipses using the eclipse_search feature 
    and displays dates on terminal. Finds the moon phase for the last day of the year
    using moon_phase. Finally checks Kepler Laws using kepler functionality
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
    print(80*"-")
    print(f"Parameters: \n{params}")
    print(80*"-")

    # All astrolist are stored
    astrolist_states = []
    step = 0

    # For the functioning of the eclipse search
    last_time_eclipse = False

    # Propagate the astrolist state for given final_state
    while astrolist.time < final_time:
        # Only show the progress if indicated to
        if params.show_progress:
            print(f"Simulation is {astrolist.time.item()/final_time*100:.3f}% complete!", end="\r")
        astrolist = verlet.advance_time(astrolist, params.interval_data_save*params.delta_time+astrolist.time)
        astrolist_states.append(astrolist.copy())
        
        #  Check for eclipses over the time of simulation
        last_time_eclipse = eclipse_check(astrolist, params.star, params.planet[0], params.satellite[0], params.planet[1], params.satellite[1], last_time_eclipse)
        step += 1
    print("                                           ", end = "\r")
    print("Simulation complete!")

    # Saves all positions in different files for each astro
    save_astros(astrolist_states)
    times = np.array([astrolist.time for astrolist in astrolist_states])
    
    # Plotting the angular momentums of each astro to check whether or not they follow keplers 2nd law
    angular_momentums = np.array([[i.angular_momentum() for i in astrolist.get_free_astros()] for astrolist in astrolist_states])
    
    for i in range(len(astrolist_states[0].get_free_astros())):
      plt.plot(times, angular_momentums[:,i,2]/np.max(np.abs(angular_momentums[:, i, 2])), label=astrolist_states[0].get_free_astros()[i].name)
    plt.title("Normalized z component of the angular momentum")
    plt.xlabel(r"$t/\text{s}$")
    plt.ylabel(r"$L_z/\text{max}(L_z)$")
    plt.legend()
    plt.savefig("output_data/angular_momentum_per_object.svg")
    if params.show_plots:
      plt.show()
    plt.clf()
    


    # Obtaining the total angular momentum for printing
    angular_momentum = np.sum(angular_momentums, axis=1)
    x_angular_momentum = np.array([a[0] for a in angular_momentum])
    y_angular_momentum = np.array([a[1] for a in angular_momentum])
    z_angular_momentum = np.array([a[2] for a in angular_momentum])
    print(80*"-") 
    print(f"Max of the angular momentum x component: {np.max(x_angular_momentum)}, minumum of the angular momentum x component: {np.min(x_angular_momentum)}")
    print(f"Max of the angular momentum y component: {np.max(y_angular_momentum)}, minumum of the angular momentum y component: {np.min(y_angular_momentum)}")
    print(f"Variation of the angular momentum z component: {(np.max(z_angular_momentum)-np.min(z_angular_momentum))/(np.mean(z_angular_momentum))}")
    
    # Plot angular momentum variation
    print(80*"-") 
    plt.plot(times, (z_angular_momentum-np.mean(z_angular_momentum))/np.mean(z_angular_momentum))
    plt.title('Relative deviation of\n the z component of total Angular momentum')
    plt.xlabel(r"$t/\text{s}$")
    plt.ylabel(r"$L_z-<L_z>/<L_z>$")
    plt.savefig('output_data/angular_momentum.svg')
    if params.show_plots:
      plt.show()
    plt.cla()

    # Delete unnecesary data to speed up the code by gainig memory space
    angular_momentum = None
    x_angular_momentum = None
    y_angular_momentum = None
    z_angular_momentum = None

    # Calculate and print total energy deviation
    total_energy = np.array([astrolist.potential for astrolist in astrolist_states]) + np.array([astrolist.kinetic_energy() for astrolist in astrolist_states])

    print(f"Variation of the energy: {(np.max(total_energy)-np.min(total_energy))/(np.mean(total_energy))}")
    print(80*"-") 

    # Show a plot with Relative deviation of the Energy
    plt.plot(times, (total_energy-np.mean(total_energy))/np.mean(total_energy))
    plt.title('Relative deviation of the Energy')
    plt.xlabel(r"$t/\text{s}$")
    plt.ylabel(r"$E-<E>/<E>$")
    plt.savefig('output_data/energy_conservation.svg')
    if params.show_plots:
      plt.show()
    plt.cla()
    total_energy = None

    # Get all astros' and CenterOfMass positions 
    positions = [[i.position for i in astrolist.get_all_astros()] for astrolist in astrolist_states]
    com = [astrolist.center_of_mass for astrolist in astrolist_states]

    # Plot the trajectory of every astro
    for i in range(len(astrolist_states[0].get_free_astros())):
        plt.plot([j[i][0] for j in positions], [j[i][1] for j in positions])
    plt.plot([i[0] for i in com], [i[1] for i in com], marker="o")
    plt.gca().set_aspect('equal')
    plt.xlabel(r"$x$/m")
    plt.ylabel(r"$y$/m")
    plt.savefig("output_data/position_output.svg")
    if params.show_plots: 
      plt.show()

    # Plot position of the COM
    plt.cla()
    plt.xlabel(r"$x$/m")
    plt.ylabel(r"$y$/m")
    plt.plot([i[0] for i in com], [i[1] for i in com])
    plt.title("COM")
    plt.savefig("output_data/COM.svg")
    if params.show_plots:
      plt.show()
    plt.cla()

    # Delete unnecesary data to speed up the code by gainig memory space
    positions = None
    com = None
    
    # Run Kepler Law Script
    kepler(astrolist_states, params.star, params.satellite[0], params.show_plots)
    plt.cla()
    print(80*"-") 

    # Check the moon phase on last day of simulation
    get_moon_phase(astrolist_states[-1],"output_data/moon_phase", params.show_plots)
    plt.cla()

    # Run the animation script
    if params.animation_step != 0:
        create_animation(astrolist_states[::params.animation_step//params.interval_data_save], "output_data/animation", params.show_progress)
    print(80*"-") 


if __name__ == "__main__":
    main()
