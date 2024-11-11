from astros import *
from verlet import *
from file_io import *
import matplotlib.pyplot as plt

print('aaa')
def main():
    solar_system = load_initial_condition("initial_conditions.ini")
    print(solar_system)
    print('hello')
    parameters = load_configuration("simulation_parameters.config")
    # print(parameters)

    # print(solar_system.second_order_func(None, np.array([[0, 1.496e11, 0], [0, 0, 0]]), None))

    # verlet = Verlet(200)

    # final_time = 365*24*3600

    # dot_interval = 24*3600 

    # positions = []

    # while solar_system.time < final_time:
    #     v, r, t = verlet.advance_time(solar_system, dot_interval+solar_system.time)
    #     solar_system.update_state(v, r, t)
    #     positions.append(r)


    # plt.plot([i[0][0] for i in positions], [i[0][1] for i in positions])
    # plt.plot([i[1][0] for i in positions], [i[1][1] for i in positions])
    # plt.plot([i[2][0] for i in positions], [i[2][1] for i in positions])
    # plt.plot([i[3][0] for i in positions], [i[3][1] for i in positions])
    # plt.plot([i[4][0] for i in positions], [i[4][1] for i in positions])
    # plt.plot([i[5][0] for i in positions], [i[5][1] for i in positions])
    # plt.plot([i[6][0] for i in positions], [i[6][1] for i in positions])
    # plt.plot([i[7][0] for i in positions], [i[7][1] for i in positions])
    # plt.show()

main()
# if __name__ == "__main__":