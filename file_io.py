# -*- coding: utf-8 -*-
"""
Script dedicated to the reading of initial conditions and simulation parameters.

Created on Wed Oct 9 2024

@author: gustavo, oscar
"""

import numpy as np
from astros import Astro, AstroList, float_type

class ConfigParams:
    """
    A class that holds simulation configuration parameters such as time steps, intervals for output,
    and other settings that control the simulation behavior
    """
    def __init__(self, params: dict):
        """
        Initialize configuration parameters from a dictionary
        Args:
            params (dict): Dictionary containing simulation configuration parameters including:
                delta_time: Time step size
                number_steps: Total number of simulation steps
                interval_print_energy: Steps between energy value prints
                interval_print_coor: Steps between coordinate prints
                plot_skip_steps: Steps to skip when plotting
                use_velocity_read: Whether to use velocity from input
        """
        self.delta_time = params["delta_time"]
        self.number_steps = params["number_steps"]
        self.animation_step = params["animation_step"]
        self.interval_data_save = params["interval_data_save"]
        self.star = params["star"]
        self.planet = params["planet"]
        self.satellite = params["satellite"]
        self.show_plots = params["show_plots"]
        self.show_progress = params["show_progress"]

    def __str__(self) -> str:
        """Returns string representation of the configuration parameters"""
        return f"  Delta time: {self.delta_time}\n  Number of steps: {self.number_steps}\n  Animation step: {self.animation_step}\n" +\
               f"  Interval data save: {self.interval_data_save}\n  Star: {self.star}\n  Planet: {self.planet}\n  Satellite: {self.satellite}\n" +\
               f"  Show plots: {self.show_plots}"

def load_initial_condition(file: str) -> AstroList:
    """
    Loads initial condition data for astronomical bodies from a file.

    Args:
        file (str): Path to input file containing initial conditions

    Returns:
        AstroList: List containing regular and fixed astronomical bodies

    The input file should contain comma-separated values for each body with:
    name, mass, x, y, z, vx, vy, vz, fixed(optional)
    """
    astros = []
    fixed_astros = []
    with open(file, "rt") as f:
        for n, line in enumerate(f.readlines()):
            # name, mass, x, y, z, vx, vy, vz, fixed
            if line.strip() == "":
                continue
            if line.strip()[0] == '#':
                continue
            values = [i.strip().lower() for i in line.split(",") if i.strip() != ""]
            if len(values) != 8 and len(values) != 9:
                raise ValueError(f"Number of values in .ini file {file} is invalid. Expected 8 or 9, got {len(values)}. Line {n+1} -> {line}")
            name = values[0].lower()
            mass = float_type(values[1])
            position = np.array([eval(i) for i in values[2:5]], dtype=float_type)
            # defaults["use_velocity_read"]
            velocity = np.array([eval(i) for i in values[5:8]], dtype=float_type)

            astro = Astro(position, velocity, mass, name)

            if len(values) == 9:
                if parse_bool(values[8], file, n, line):
                    fixed_astros.append(astro)
                    continue
                else:
                    astros.append(astro)
                    continue
            astros.append(astro)

    return AstroList(astros, fixed_astros)


def load_configuration(file: str) -> ConfigParams:
    """
    Loads simulation configuration parameters from a file.

    Args:
        file (str): Path to configuration file

    Returns:
        ConfigParams: Object containing simulation parameters

    The configuration file should contain key-value pairs for parameters.
    Default values are used for any parameters not specified in the file.
    """
    defaults = {"delta_time": 3600, "number_steps": 365*24, "animation_step": 0, "star": "", "planet": ("", 0), "satellite": ("", 0), "interval_data_save": 1, "show_plots": True, "show_progress": True}

    with open(file, "rt") as f:
        for n, line in enumerate(f.readlines()):
            if line.strip() == "":
                continue
            if line.strip()[0] == '#':
                continue

            line_parts = line.split()
            key, value = line_parts[0].lower().strip(), "".join(line_parts[1:]).strip()
            for k in defaults.keys():
                if key == k:
                    if k == "delta_time":
                        defaults[k] = float(eval(value))
                    elif k == "star":
                        defaults[k] = value.strip()
                    elif k == "planet" or k == "satellite":
                        parts = value.strip().split(",")
                        defaults[k] = (parts[0].strip(), float(eval(parts[1].strip())))
                    elif k == "show_plots":
                        defaults[k] = parse_bool(value, file, n, line)
                    elif k == "show_progress":
                        defaults[k] = parse_bool(value, file, n, line)
                    else:
                        defaults[k] = int(eval(value))

    return ConfigParams(defaults)

def parse_bool(value: str, file: str, line_number: int, line: str) -> bool:
    """
    Parse a string value into a boolean.

    Args:
        value (str): String to parse ("true" or "false")
        file (str): Source file name for error reporting
        line_number (int): Line number for error reporting
        line (str): Full line content for error reporting

    Returns:
        bool: Parsed boolean value

    Raises:
        ValueError: If value is not "true" or "false"
    """
    value = value.lower().strip()
    if value in {"true", "false"}:
        return value == "true"
    else:
        raise ValueError(f"Unknown bool value \"{value}\" in line {line_number+1} of the file {file} -> {line}")
