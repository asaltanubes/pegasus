# -*- coding: utf-8 -*-
"""
There are three Kepler laws:
1. Orbits ara elipses with one of the focus on the center of mass
2. The body1-body2 vector swipes equal areas in equal times,
    which is equivalent to angular momentum, that has been proved using plots
3. The cube of the period T^3 is proportional to R^2

This scipt is dedicated to proving the 3rd Kepler Law

Created on Wed Dic 4 2024

@author: gustavo
"""
 

import numpy as np
from astros import AstroList, Astro
import matplotlib.pyplot as plt



def half_year_indices(list_astros: list[Astro]) -> list[int]:
    """
    Given a list contanining astros that moove around the center of mass
    compute the indices corresponding to when half a year of the orbit is corssed.

    In order to compute half a year intervals the algorithm used starts by computing
    a vector that is perpendicular to the initial position vector in COM coordinates
    and in the plane of the movement of the astro defined by the position and the velocity.
   
    Using this vector u half a year corresponds to a zero on the dot product <r, u> with r
    the position vector in center of mass coordinates.

    Args:
        list_astros (list[Astro]): A list containing the astro object in each timestep.

    Returns:
        list[int]: indices of the points corresponding to half a year intervals of the 
                   orbit of the astro. 
    """

    # Consturcting the position list and the vector u    
    positions = [i.pos_com for i in list_astros]
    initial_velocity = list_astros[0].velocity
    initial_r = positions[0]
    # this corresponds to the vector u
    mul_vector = initial_r + np.dot(initial_r, initial_r)/np.dot(initial_velocity, initial_r) * initial_velocity

    # Since the position vector list can be interpreted as a matrix of the form
    #
    #              (r_x0, r_y0, r_z0)
    #              (r_x1, r_y1, r_z1)
    # positions =  (r_x2, r_y2, r_z2)
    #              (r_x3, r_y3, r_z3)
    #              (r_x4, r_y4, r_z4)
    # 
    # the dot product list corresponds to the matrix multiplication of positions 
    # with the u vector (mul_vector)
    
    dots = positions@mul_vector

    # To find the zeros we can use the continuity of the dot product 
    # (both r and u are continuos) and Aplying bolzano's theorem we search for sign changes
    # this is easyer to do with numpy by search when the product of an element with the next 
    # (dots[i+1] * dots[i]) is negative since same sign multiplication is always positive. 
    zero_arrays = dots[1:]*dots[:-1]
    indices = np.argwhere(zero_arrays <= 0)

    # The flatten prevents the return value from being a column vector  
    return indices.flatten()

    
            

def kepler(list_astros: list[AstroList], star_name: str, satellite_name: str, show_plot: bool = True):
    """
    Given a list of astrolists repesenting a solar system generates a graph with the ln of the semi-mayor axis
    against the ln of the period. This allows to check the relationship a propto T^alpha where we expect 
    alpha = 1.5. The plot is also saved in output_data in svg format.
    
    The star of the system and the satelite provided for checking for eclipses are removed from the plot since
    the movement of neither of these can be aproximated as a two body sistem so they dont follow the third kepler law.
    
    args:
        list_astros (list[AstroList]): A list of the astrolist in each timestep.
        star_name (str): The name of the star of the system
        satellite_name (str): The name of the satelite of the system
        show_plot (bool): whether or not to show the plot or just save it
    """
    # obtain the positions for all of the free astros that are not the star or the satellite and the indices where a half a year multiple has passed
    time_array = np.array([astro.time for astro in list_astros])
    astros = np.transpose([[astro for astro in astrolist.get_free_astros() if astro.name != star_name and astro.name != satellite_name] for astrolist in list_astros])
    half_year_times = [half_year_indices(astro_times) for astro_times in astros]

    # get which astros have at least one datapoint for plotting and if not enough astros have data dont do the plot
    which_astros_have_half_a_year = [len(i)>=2 for i in half_year_times]
    if len([i for i in which_astros_have_half_a_year if i]) < 2:
        print("Not enough data for kepler simulation")
        return

    # list containing the times when half a year has passed from last datapoint
    half_year_time_arrays = [time_array[half_year_by_planet] for astro_has_enough_data, half_year_by_planet in 
                                        zip(which_astros_have_half_a_year, half_year_times) if astro_has_enough_data]
    # compute the average year duration for each astro
    mean_year_duration = 2*np.array([np.mean(half_year_times[1:]-half_year_times[:-1]) for half_year_times in half_year_time_arrays])

    # compute the semi mayor axis length
    positions = np.array([[i.pos_com for i in astro_times] for astro_has_enough_data, astro_times in zip(which_astros_have_half_a_year, astros) if astro_has_enough_data])
    radious_norm_max = np.max(np.array(np.linalg.norm(positions, axis=2)), axis=1)

    # plotting and linear fit
    plt.scatter(np.log(radious_norm_max), np.log(mean_year_duration))
    print(f"Correlation coefficient of the log(a) log(T) graph from kepler: {r(np.log(radious_norm_max), np.log(mean_year_duration)):.5f}")
    pen, dpen, n0, dn0 = least_squares(np.log(radious_norm_max), np.log(mean_year_duration))
    xx = np.linspace(np.min(np.log(radious_norm_max)), np.max(np.log(radious_norm_max)))
    print(f"The linear regression from the kepler data is y = ({pen:.5f} ± {dpen:.5f})x + ({n0:.5f} ± {dn0:.5f})")
    plt.plot(xx, pen*xx+n0, c="red", zorder=-1)
    plt.xlabel(r"$\ln(a/\text{m})$")
    plt.ylabel(r"$\ln(T/\text{s})$")
    plt.axis("auto")
    plt.title(f"Slope = {pen:.3f}±{dpen:.3f} n0 = {n0:.3f}±{dn0:.3f}")
    plt.savefig("output_data/kepler.svg")
    if show_plot:
        plt.show()


def r(x: list[float], y: list[float]):
    """
    Computes the correlation coefficient for a linear regression from the x and y values of the datapoints.
    Args: 
        x: list[float] x values of the datapoints
        y: list[float] y values of the datapoints
    """
    x = np.array(x)
    y = np.array(y)
    des_x = x - x.mean()
    des_y = y - y.mean()
    sigma_x = sum(des_x**2)
    sigma_y = sum(des_y**2)
    return sum(des_x * des_y)/np.sqrt(sigma_x*sigma_y)


def least_squares(x: list[float], y: list[float]) -> tuple[float, float, float, float]:
    """
    Calculates the line of adjustment by least squares for two lists using the analitic formulas.
    """
    x = np.array(x)
    y = np.array(y)
    n = len(x)
    sum_x: float = np.sum(x)
    sum_y: float = np.sum(y)
    sum_xy: float = np.sum(x*y)
    sum_x2: float = np.sum(x*x)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)

    n0 = (sum_y * sum_x2 - sum_x * sum_xy) / (n * sum_x2 - sum_x ** 2)

    sigma_y = np.sqrt(np.sum((y - (slope * x + n0)) ** 2 / (n - 2)))

    sigma_slope = sigma_y * np.sqrt(n / (n * sum_x2 - sum_x ** 2))
    sigma_n0 = sigma_y * np.sqrt(sum_x2 / (n * sum_x2 - sum_x ** 2))

    return (slope, sigma_slope, n0, sigma_n0)
