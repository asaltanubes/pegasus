from astros import *
from verlet import *
from file_io import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    astrolist = load_initial_condition("initial_conditions.ini")

    params = load_configuration("simulation_parameters.conf")

    verlet = Verlet(params.delta_time)

    final_time = params.delta_time * params.number_steps

    positions = []
    potential = []
    kinetic_energy=[]
    times = []

    print(f"Initial conditions \n {astrolist}")
    print()
    print(f"Parameters: \n{params}")

    while astrolist.time < final_time:
        astrolist = verlet.advance_time(astrolist, params.delta_time+astrolist.time)
        earth = astrolist.get_free_astros()[0]
        positions.append(earth.position)
        kinetic_energy.append(1/2 * earth.mass*np.linalg.norm(earth.velocity)**2)
        potential.append(astrolist.potential) 
        times.append(astrolist.time)

    potential = np.array(potential)
    kinetic_energy = np.array(kinetic_energy)
    total_energy = potential+kinetic_energy

    print(f"Variation of the energy: {(np.max(total_energy)-np.min(total_energy))/(np.mean(total_energy))}")

    with open("positions_output.txt", "wt") as file:
        file.write("\n".join([", ".join([str(j) for j in i]) for i in positions]))
    plt.plot([i[0] for i in positions], [i[1] for i in positions])
    plt.plot(0,0,'or')
    plt.gca().set_aspect('equal')
    plt.show()

    plt.plot(times, total_energy)
    plt.show()

    

if __name__ == "__main__":
    main()