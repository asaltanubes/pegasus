import numpy as np
import matplotlib.pyplot as plt

float_type = np.longdouble

# def gravitational_pull(i_position: np.ndarray, j_position: np.ndarray, i_mass: float_type, j_mass: float_type):
#     G = float_type(6.6743e-11)
#     r = j_position-i_position
#     return G * i_mass*j_mass/(np.linalg.norm(r)**3)*r

class Astro:
    def __init__(self, position: tuple[float, float, float], velocity: tuple[float, float, float], mass: float, name: str = ''):
        self.position = np.array(position, dtype=float_type)
        self.pos_com = np.array([0, 0, 0], dtype=float_type)
        self.velocity = np.array(velocity, dtype=float_type)
        self.mass = float_type(mass)
        self.name = name

        self.force = np.array([0.0, 0.0, 0.0], dtype=float_type)
        self.potential = np.array(0, dtype=float_type)


    # def gravitational_pull_over_self(self, other) -> np.array:
    #     return gravitational_pull(self.position, other.position, self.mass, other.mass)

    def reset_force(self):
        self.force = 0*self.force
    def reset_potential(self):
        self.potential = 0*self.potential

    def kinetic_energy(self):
        return 1/2*self.mass*np.linalg.norm(self.velocity)**2

    def angular_momentum(self):
        return self.mass*np.cross(self.position, self.velocity)

    def __str__(self):
        return (f"{self.name}, "if self.name!='' else "") + f'mass: {self.mass}, position: {self.position}, velocity: {self.velocity}'

    def __repr__(self):
        return f"Astro({self})"
    def copy(self):
        astro_copy = Astro(self.position.copy(), self.velocity.copy(), self.mass.copy(), self.name)
        astro_copy.force = self.force.copy()
        astro_copy.potential = self.potential.copy()
        astro_copy.pos_com = self.pos_com.copy()
        return astro_copy



class AstroList:
    def __init__(self, astros: list[Astro], fixed_astros: list[Astro] = [], time=0):
        self.__astros = np.array(astros)
        self.__fixed_astros = np.array(fixed_astros)
        self.potential = np.longdouble(0)
        self.time = float_type(time)
        self.center_of_mass = np.array([0, 0, 0], dtype=float_type)

    def reset_forces(self):
        for i in self.__astros:
            i.reset_force()

    def reset_potentials(self):
        for i in self.__astros:
            i.reset_potential()
        for i in self.__fixed_astros:
            i.reset_potential()


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

        G = float_type(6.6743e-11)
        masses = self.masses()
        position_and_masses = [[y[i], masses[i]] for i in range(len(y))]
        self.potential = 0*self.potential
        # forces = np.zeros((len(self.__astros), 3), dtype=float_type)
        self.reset_forces()
        self.reset_potentials()
        for i in range(len(self.__astros)):
            astro_i = self.__astros[i]
            i_pos, i_mass = position_and_masses[i]
            for j in range(i+1, len(self.__astros)):
                astro_j = self.__astros[j]
                j_pos, j_mass = position_and_masses[j]
                r = j_pos-i_pos
                inv_r = 1/np.linalg.norm(r)
                force = G * i_mass*j_mass*inv_r**3*r
                astro_i.force += force
                astro_j.force -= force
                potential =  -G * i_mass*j_mass*inv_r
                astro_i.potential += potential
                self.potential += potential
                astro_j.potential += potential


        if self.__fixed_astros.size > 0:
            for fixed_astro in self.__fixed_astros:
                for i in range(len(self.__astros)):
                    free_astro = self.__astros[i]
                    i_pos, i_mass = position_and_masses[i]
                    j_pos = fixed_astro.position
                    j_mass = fixed_astro.mass
                    r = j_pos-i_pos
                    inv_r = 1/np.linalg.norm(r)
                    force = G * i_mass*j_mass*inv_r**3*r
                    potential =  -G * i_mass*j_mass*inv_r
                    free_astro.force += force
                    fixed_astro.force -= force
                    free_astro.potential += potential
                    self.potential += potential
                    fixed_astro.potential += potential
        return np.array([self.__astros[i].force/masses[i] for i in range(len(self.__astros))])

    def update_state(self, yp, y, t, forces = None, potentials = None):
        self.center_of_mass = np.sum([i.mass*i.position for i in self.get_all_astros()], axis=0)/np.sum(self.masses())
        for (astro, v, r) in zip(self.__astros, yp, y):
            astro.position = r
            astro.com_pos = astro.position-self.center_of_mass
            astro.velocity = v
            # astro.force = f
            # astro.potential = p

        self.time = t



    def kinetic_energy(self):
        return np.sum(i.kinetic_energy() for i in self.__astros)

    def angular_momentum(self):
        return np.sum(i.angular_momentum() for i in self.__astros)

    def positions_2d(self):
        return [i.position[0:2].copy() for i in self.__astros]

    def velocities_2d(self):
        return [i.velocity[0:2].copy() for i in self.__astros]
    def masses(self):
        return [i.mass for i in self.get_all_astros()]

    def get_all_astros(self):
        return np.append(self.__fixed_astros, self.__astros)

    def get_astro_by_name(self, name):
        return next(i for i in self.get_all_astros() if i.name==name)

    def get_free_astros(self):
        return self.__astros

    def get_fixed_astros(self):
        return self.__fixed_astros

    def copy(self):
        fixed_astros = [astro.copy() for astro in self.__fixed_astros]
        free_astros = [astro.copy() for astro in self.__astros]
        return AstroList(free_astros, fixed_astros, self.time)

    def __str__(self):
        return f"AstroList:\n  Free astros:\n    "+"\n    ".join(str(i) for i in self.__astros)+"\n  Fixed astros:\n    " + "\n    ".join(str(i) for i in self.__fixed_astros)

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
