import numpy as np
from astros import AstroList, Astro



def new_year(list_astros: list[AstroList]) -> float:
    theta_0 = [np.arctan2(astro.position[1], astro.position[0]) for astro in list_astros[0].get_all_astros()]

    theta = [np.arctan2(astro.position[1], astro.position[0]) for astro in list_astros[0].get_all_astros()]
    # if np.abs(theta0_earth-theta_earth) < np.pi/(360*12):
    #     print(f"New year!: {astrolist.time/(3600*24)} day")

    for astrolist in list_astros:
        for astro in astrolist:
            


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
