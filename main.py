from astros import *
from verlet import *
from file_io import *
import matplotlib.pyplot as plt

def main():
    astrolist = load_initial_condition("initial_conditions.ini")

    params = load_configuration("simulation_parameters.conf")

    verlet = Verlet(params.delta_time)

    final_time = params.delta_time * params.number_steps

    positions = []
    potential = []

    while astrolist.time < final_time:
        v, r, t = verlet.advance_time(astrolist, params.delta_time+astrolist.time)
        astrolist.update_state(v, r, t)
        positions.append(r)
        potential.append(astrolist.potential) 


    plt.plot([i[0][0] for i in positions], [i[0][1] for i in positions])
    plt.plot(0,0,'or')
    plt.show()

    plt.plot(range(0, len(potential)),potential,'ob')
    plt.show()

    

if __name__ == "__main__":
    main()