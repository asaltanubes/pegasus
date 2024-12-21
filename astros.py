# -*- coding: utf-8 -*-
"""
Astro and Astrolist classes are defined in this script 

All units are in SI

Created on Wed Oct 9 2024

@author: gustavo
"""



import numpy as np

float_type = np.longdouble

class Astro:
    """
    Class representing an astronomical object with position, velocity, mass and other physical properties.

    This class provides functionality to track and update the physical state of an astronomical body,
    including its position, velocity, mass, forces acting on it, and potential/kinetic energy.
    It supports operations needed for gravitational calculations and N-body simulations.
    """
    def __init__(self, position: tuple[float, float, float], velocity: tuple[float, float, float], mass: float, name: str = ''):
        """
        Initialize an astronomical object with position, velocity, mass and optional name.

        Args:
            position: Initial (x,y,z) position in m as a tuple of floats
            velocity: Initial (vx,vy,vz) velocity in m as a tuple of floats
            mass: Mass of the object in kg as a float
            name: Optional name string for the object

        Initializes position, velocity and mass arrays, as well as zeroed force and potential arrays.
        Position relative to center of mass (pos_com) is initialized at origin.
        """
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
        """Resets the force vector to zero"""
        self.force = 0*self.force

    def reset_potential(self):
        """Resets the potential energy to zero"""
        self.potential = 0*self.potential

    def kinetic_energy(self) -> float_type:
        """Calculates and returns the kinetic energy of the astronomical object using 1/2*m*v^2"""
        return 1/2*self.mass*np.linalg.norm(self.velocity)**2

    def angular_momentum(self) -> float_type:
        """Calculates and returns the angular momentum with respect to the center of mass using mass*cross(position, velocity)"""
        return self.mass*np.cross(self.position, self.velocity)

    def __str__(self) -> str:
        """Returns string representation of the astronomical object including name (if exists), mass, position and velocity"""
        return (f"{self.name}, "if self.name!='' else "") + f'mass: {self.mass}, position: {self.position}, velocity: {self.velocity}'

    def __repr__(self) -> str:
        """Returns formal string representation using the Astro class name"""
        return f"Astro({self})"

    def copy(self):
        """Creates and returns an independent copy of the astronomical object with all attributes copied"""
        astro_copy = Astro(self.position.copy(), self.velocity.copy(), self.mass.copy(), self.name)
        astro_copy.force = self.force.copy()
        astro_copy.potential = self.potential.copy()
        astro_copy.pos_com = self.pos_com.copy()
        return astro_copy



class AstroList:
    """
    Class representing a collection of astronomical objects, both fixed and free-moving.

    This class manages a system of astronomical bodies, handling their gravitational interactions,
    energy calculations, and state updates. It supports both fixed objects (stationary in space)
    and free objects that move under gravitational forces.

    The class provides methods for:
    - Force and potential calculations between objects
    - System state updates
    - Energy and momentum calculations
    - Position and velocity tracking
    - Object management
    """
    def __init__(self, astros: list[Astro], fixed_astros: list[Astro] = [], time=0):
        """
        Initialize AstroList with list of astronomical objects, fixed objects, time and initializes internal arrays.

        Args:
            astros: List of freely moving astronomical objects
            fixed_astros: Optional list of stationary astronomical objects, defaults to empty list
            time: Initial time value for the system, defaults to 0

        Initializes both the free and fixed astros, as well as zeroed potential array.
        Position of the center of mass is initialized at origin.
        """
        self.__astros = np.array(astros)
        self.__fixed_astros = np.array(fixed_astros)
        self.potential = float_type(0)
        self.time = float_type(time)
        self.center_of_mass = np.array([0, 0, 0], dtype=float_type)

    def reset_forces(self):
        """Reset forces to zero for all non-fixed astronomical objects"""
        for astro in self.__astros:
            astro.reset_force()

    def reset_potentials(self):
        """Reset potentials to zero for all astronomical objects (fixed and non-fixed)"""
        for free_astro in self.__astros:
            free_astro.reset_potential()
        for fixed_astro in self.__fixed_astros:
            fixed_astro.reset_potential()

    def update_forces(self):
        """Calculate and update gravitational forces between all pairs of celestial bodies"""
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

    def second_order_initial_conditions(self) -> tuple[list, list, float_type]:
        """Get initial conditions for second order differential equation solver"""
        yp = [i.velocity for i in self.__astros]
        y  = [i.position for i in self.__astros]
        return (yp, y, self.time)

    def second_order_func(self, y) -> np.ndarray:
        """
        Calculate gravitational forces and potentials between all objects for second order solver,
        uses the positions given in y instead of the ones in the astros. 

        Also updates the potentials and the forces

        Args:
            y: List of positions for each object

        Returns:
            An array of the accelerations of all the free astros

        """

        G = float_type(6.6743e-11)
        masses = self.masses()
        position_and_masses = [[y[i], masses[i]] for i in range(len(y))]
        self.potential = 0*self.potential
        self.reset_forces()
        self.reset_potentials()
        # double loop for free astros
        for i in range(len(self.__astros)):
            astro_i = self.__astros[i]
            i_pos, i_mass = position_and_masses[i]
            for j in range(i+1, len(self.__astros)):
                astro_j = self.__astros[j]
                j_pos, j_mass = position_and_masses[j]
                r = j_pos-i_pos
                inv_r = 1/np.linalg.norm(r)

                # computing force
                force = G * i_mass*j_mass*inv_r**3*r
                astro_i.force += force
                astro_j.force -= force

                # computing potential
                potential =  -G * i_mass*j_mass*inv_r
                astro_i.potential += potential
                self.potential += potential
                astro_j.potential += potential
        # double loop using the fixed astros
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

    def update_state(self, yp, y, t):
        """
        Updates the postitions, velocities and time of the AstroList
        
        Args:
            yp: List of velocities for each object
            y: List of positions for each object
            t: Current time value
        """
        self.center_of_mass = np.sum([i.mass*i.position for i in self.get_all_astros()], axis=0)/np.sum(self.masses())
        for (astro, v, r) in zip(self.__astros, yp, y):
            astro.position = r
            astro.pos_com = astro.position-self.center_of_mass
            astro.velocity = v

        self.time = t

    def kinetic_energy(self) -> float_type:
        """Calculate total kinetic energy of all non-fixed objects"""
        return np.sum(i.kinetic_energy() for i in self.__astros)

    def angular_momentum(self) -> float_type:
        """Calculate total angular momentum of all non-fixed objects"""
        return np.sum(i.angular_momentum() for i in self.__astros)

    def positions_2d(self) -> list[np.array]:
        """Get 2D positions (x,y components) of all non-fixed objects"""
        return [i.position[0:2].copy() for i in self.__astros]

    def velocities_2d(self) -> list[np.array]:
        """Get 2D velocities (x,y components) of all non-fixed objects"""
        return [i.velocity[0:2].copy() for i in self.__astros]

    def masses(self) -> list[float_type]:
        """Get list of masses of all objects (fixed and non-fixed)"""
        return [i.mass for i in self.get_all_astros()]

    def get_all_astros(self):
        """Get array containing all astronomical objects (fixed and non-fixed)"""
        return np.append(self.__fixed_astros, self.__astros)

    def get_astro_by_name(self, name: str) -> Astro:
        """
        Get astronomical object by its name

        Args:
            name: Name of the desired astro
        """
        return next(i for i in self.get_all_astros() if i.name==name)

    def get_free_astros(self):
        """Get array of non-fixed astronomical objects"""
        return self.__astros

    def get_fixed_astros(self):
        """Get array of fixed astronomical objects"""
        return self.__fixed_astros

    def copy(self):
        """Create an independent copy of the AstroList instance"""
        fixed_astros = [astro.copy() for astro in self.__fixed_astros]
        free_astros = [astro.copy() for astro in self.__astros]
        alist = AstroList(free_astros, fixed_astros, self.time)
        alist.center_of_mass = self.center_of_mass.copy()
        alist.potential=self.potential.copy()
        return alist

    def __str__(self) -> str:
        """Get string representation of AstroList showing fixed and non-fixed objects"""
        return f"AstroList:\n  Free astros:\n    "+"\n    ".join(str(i) for i in self.__astros)+"\n  Fixed astros:\n    " + "\n    ".join(str(i) for i in self.__fixed_astros)
