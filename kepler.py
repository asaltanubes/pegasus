# -*- coding: utf-8 -*-
"""
Script dedicated to...

Created on Wed Dic 4 2024

@author: gustavo
"""
 

import numpy as np
from astros import AstroList, Astro
import matplotlib.pyplot as plt



def new_year(list_astros: list[Astro]) -> float:
    positions = [i.pos_com for i in list_astros]
    initial_velocity = list_astros[0].velocity
    initial_r = positions[0]

    mul_vector = initial_r + np.dot(initial_r, initial_r)/np.dot(initial_velocity, initial_r) * initial_velocity

    dots = positions@mul_vector
    # Aplying bolzano's theorem
    zero_arrays = dots[1:]*dots[:-1]
    indices = np.argwhere(zero_arrays <= 0)
    
    return indices.flatten()

    
            

def kepler(list_astros: list[AstroList], star_name: str, satellite_name: str, show_plot: bool = True):
    """
    'Description'
    
    Args:
        arg_1 (class): description

    Returns (type):  
        Description
    
    """
    time_array = np.array([astro.time for astro in list_astros])
    astros = np.transpose([[astro for astro in astrolist.get_free_astros() if astro.name != star_name and astro.name != satellite_name] for astrolist in list_astros])
    half_year_times = [new_year(astro_times) for astro_times in astros]

    which_astros_have_half_a_year = [len(i)>=2 for i in half_year_times]
    if len([i for i in which_astros_have_half_a_year if i]) < 2:
        print("Not enough data for kepler simulation")
        return

    half_year_time_arrays = [time_array[half_year_by_planet] for astro_has_enough_data, half_year_by_planet in 
                                        zip(which_astros_have_half_a_year, half_year_times) if astro_has_enough_data]
    mean_year_duration = 2*np.array([np.mean(half_year_times[1:]-half_year_times[:-1]) for half_year_times in half_year_time_arrays])
    positions = np.array([[i.pos_com for i in astro_times] for astro_has_enough_data, astro_times in zip(which_astros_have_half_a_year, astros) if astro_has_enough_data])
    radious_norm_max = np.max(np.array(np.linalg.norm(positions, axis=2)), axis=1)
    plt.scatter(np.log(radious_norm_max), np.log(mean_year_duration))
    print(r(np.log(radious_norm_max), np.log(mean_year_duration)))
    pen, dpen, n0, dn0 = least_squares(np.log(radious_norm_max), np.log(mean_year_duration))
    print(pen, dpen, n0, dn0)
    xx = np.linspace(np.min(np.log(radious_norm_max)), np.max(np.log(radious_norm_max)))
    plt.plot(xx, pen*xx+n0, c="red", zorder=-1)
    plt.xlabel(r"$\ln(a/\text{m})$")
    plt.ylabel(r"$\ln(T/\text{s})$")
    plt.title(f"Slope = {pen:.3f}±{dpen:.3f} n0 = {n0:.3f}±{dn0:.3f}")
    plt.savefig("output_data/kepler.svg")
    if show_plot:
        plt.show()


def r(x: list[float], y: list[float]):
    x = np.array(x)
    y = np.array(y)
    des_x = x - x.mean()
    des_y = y - y.mean()
    sigma_x = sum(des_x**2)
    sigma_y = sum(des_y**2)
    return sum(des_x * des_y)/np.sqrt(sigma_x*sigma_y)


def least_squares(x: list[float], y: list[float]) -> tuple[float, float, float, float]:
    """
    Calculates the line of adjustment by least squares for two lists.

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
