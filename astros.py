import numpy as np
import matplotlib.pyplot as plt
from diff_eq import SecondOrderEdo

float_type = np.longdouble

def gravitational_pull(i_position: np.ndarray, j_position: np.ndarray, i_mass: float_type, j_mass: float_type):
    G = float_type(6.6743e-11)
    r = j_position-i_position
    return G * i_mass*j_mass/(np.linalg.norm(r)**3)*r

class Astro:
    def __init__(self, position: tuple[float, float, float], velocity: tuple[float, float, float], mass: float, name: str = ''):
        self.position = np.array(position, dtype=float_type)
        self.velocity = np.array(velocity, dtype=float_type)
        self.mass = float_type(mass)
        self.name = name

        self.force = np.array([0.0, 0.0, 0.0], dtype=float_type)

    
    def gravitational_pull_over_self(self, other) -> np.array:
        return gravitational_pull(self.position, other.position, self.mass, other.mass)
    
    def reset_force(self):
        self.force = 0*self.force

    def __str__(self):
        return (f"{self.name}, "if self.name!='' else "") + f'position: {self.position}, speed: {self.velocity}, mass: {self.mass}' 
    
    def __repr__(self):
        return f"Astro({self})"

class AstroList(SecondOrderEdo):
    def __init__(self, astros: list[Astro], fixed_astros: list[Astro] = [], time=0):
        self.__astros = np.array(astros)
        self.__fixed_astros = np.array(fixed_astros)
        self.time = float_type(time)
    
    def reset_forces(self):
        for i in self.__astros:
            i.reset_force()
    
    def update_forces(self):
        self.reset_forces()
        list_iter = self.__astros.copy()
        for i in reversed(list_iter):
            list_iter.remove(i)
            for j in list_iter:
                f = i.gravitational_pull_over_self(j)
                i.force += f
                j.force -= f
        # If we have fixed astros make them interact with all of the other astros
        if self.__fixed_astros.size > 0:
            for i in self.__fixed_astros:
                for j in self.__astros:
                    f = j.gravitational_pull_over_self(i)
                    j.force += f

    def second_order_initial_conditions(self):
        yp = [i.velocity for i in self.__astros]
        y  = [i.position for i in self.__astros]
        x  = np.longdouble(0)
        return (yp, y, self.time)
    
    def second_order_func(self, yp, y, x):
        masses = self.masses()
        position_and_masses = [[y[i], masses[i]] for i in range(len(y))]
        forces = np.zeros((len(self.__astros), 3), dtype=float_type)
        for i in range(len(forces)):
            i_pos, i_mass = position_and_masses[i] 
            for j in range(i+1, len(forces)):
                j_pos, j_mass = position_and_masses[j]
                force = gravitational_pull(i_pos, j_pos, i_mass, j_mass)
                forces[i] += force
                forces[j] -= force

        if self.__fixed_astros.size > 0:
            for fixed_astro in self.__fixed_astros:
                for i in range(len(forces)):
                    i_pos, i_mass = position_and_masses[i]
                    force = gravitational_pull(i_pos, fixed_astro.position, i_mass, fixed_astro.mass)
                    forces[i] += force
                    
        return np.array([forces[i]/masses[i] for i in range(len(forces))])
    
    def update_state(self, yp, y, t):
        for (astro, v, r) in zip(self.__astros, yp, y):
            astro.position = r
            astro.velocity = v
        
        self.time = t
                    

        

    def positions_2d(self):
        return [i.position[0:2].copy() for i in self.__astros]

    def velocities_2d(self):
        return [i.velocity[0:2].copy() for i in self.__astros]
    def masses(self):
        return [i.mass for i in self.__astros]

# sol = Astro([0, 0, 0], [0, 0, 0], 1.989e30)
# tierra = Astro([150e9, 0, 0], [0, 29800, 0], 5.972e24)

# solar_system = AstroList([sol, tierra])

# s = []
# t = []
# vs = []
# vt = []

# dt = 20
# n  = 365
# import time
# start = time.time()
# simtime = 365*24*3600/n
# for i in range(n):
#     solar_system.simulate(simtime, dt)
#     posi = solar_system.positions_2d()
#     vel = solar_system.velocities_2d()
#     s.append(posi[0])
#     t.append(posi[1])
#     vs.append(vel[0])
#     vt.append(vel[1])
# end = time.time()
# print("simulation_complete")

# print(end-start)

# Lt = np.array([(pos[0]*vel[1]-pos[1]*vel[0])*tierra.mass for pos, vel in zip(t, vt)])
# Ls = np.array([(pos[0]*vel[1]-pos[1]*vel[0])*sol.mass for pos, vel in zip(s, vs)])
# Ltotal = Ls+Lt


# plt.scatter([i[0] for i in s], [i[1] for i in s])

# plt.plot([i[0] for i in t], [i[1] for i in t])

# # ax = plt.gca()
# # ax.set_aspect('equal', adjustable='box')

# plt.show()

# print(f"Relative error in Lt: {(max(Lt)-min(Lt))/sum(Lt)*len(Lt)}")
# print(f"Relative error in Ls: {(max(Ls)-min(Ls))/sum(Ls)*len(Ls)}")
# print(f"Relative error in Ltotal: {(max(Ltotal)-min(Ltotal))/sum(Ltotal)*len(Ltotal)}")

# times = [simtime*i for i in range(n)]
# plt.plot(times, Lt, label="Tierra")
# # plt.plot(times, Ls, label="Sol")
# plt.plot(times, Ltotal, label="total")
# plt.legend()
# plt.show()