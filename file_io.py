import numpy as np

from astros import Astro, AstroList

class ConfigParams:
    def __init__(self, params: dict):
        self.delta_time = params["delta_time"]
        self.number_steps = params["number_steps"]
        self.interval_print_energy = params["interval_print_energy"]
        self.interval_print_coor = params["interval_print_coor"]
        self.plot_skip_steps = params["plot_skip_steps"]
        self.use_velocity_read = params["use_velocity_read"]



def load_initial_condition(file: str) -> AstroList:
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
                raise ValueError(f"Number of values in .ini file {file} is invalid expected 8 or 9 got {len(values)} in line {n+1} -> {line}")
            position = np.array(values[2:5], dtype=np.longdouble)
            velocity = np.array(values[5:8], dtype=np.longdouble)
            name = values[0].lower()
            mass = np.longdouble(values[1])
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
    defaults = {"delta_time": 420, "number_steps": 400000, "interval_print_energy": 10000, "interval_print_coor": 10000, "plot_skip_steps": 100, "use_velocity_read": False}

    with open(file, "rt") as f:
        for n, line in enumerate(f.readlines()):
            if line.strip() == "":
                continue
            if line.strip()[0] == '#':
                continue

            key, value = line.split()
            for (k, _) in defaults.items():
                if key.lower().strip() == k:
                    if k == "use_velocity_read":
                        defaults[k] = parse_bool(value, file, n, line)
                    elif k == "delta_time":
                        defaults[k] = float(value)
                    else:
                        defaults[k] = int(value)

    return ConfigParams(defaults)

def parse_bool(value: str, file: str, line_number: int, line: str) -> bool:
    value = value.lower().strip()
    if value in {"true", "false"}:
        if value == "true":
            return True
        else:
            return False
    else:
        raise ValueError(f"Unknown bool value \"{value}\" in line {line_number+1} of the file {file} -> {line}")
