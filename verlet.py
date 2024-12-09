# -*- coding: utf-8 -*-
import numpy as np
from astros import AstroList, float_type

class Verlet():
    """Velocity Verlet integration method implementation"""
    def __init__(self, stepsize: float):
        """
        Initialize Verlet integrator with given stepsize

        Args:
            stepsize (float): Time step for integration
        """
        self.stepsize = float_type(stepsize)

    def advance_time(self, astrolist: AstroList, t_final: float) -> AstroList:
        """
        Advance system state using velocity Verlet algorithm

        Args:
            astrolist (AstroList): List of astronomical bodies to integrate
            t_final (float): Time to integrate until

        Returns:
            Updated astrolist with new positions and velocities
        """
        func = lambda yp, y, x: astrolist.second_order_func(yp, y, x)
        yp0, y0, t0 = astrolist.second_order_initial_conditions()
        delta_t = np.array([self.stepsize])

        number_of_steps = (t_final-t0)//delta_t
        final_time = number_of_steps*delta_t + t0

        r = y0.copy()
        v = yp0.copy()
        a = func(v, r, t0)
        delta_t2 = delta_t**2

        for i in range(1, int(number_of_steps)+1):
            r += v*delta_t + a*delta_t2/2
            v += a/2 * delta_t
            a = func(v, r, t0 + i*delta_t)
            v += a/2 * delta_t

        astrolist.update_state(v, r, final_time)

        return astrolist
