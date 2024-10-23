from abc import ABC
from abc import abstractmethod
import numpy as np
class FirstOrderEDO(ABC):
    """
    Represents a first order edo of the form
    y' = f(y, x)
    """
    @abstractmethod
    def first_order_func(self, y, x):
        """ 
        Given an equation of the form y' = f(y, x) this function returns f
        """
        pass
    @abstractmethod
    def first_order_initial_conditions(self):
        """Returns the initial condition for x and y as (y, x)
        """
        pass 

class SecondOrderEdo(FirstOrderEDO):
    """Represents a second order diferential equation of the form y'' = f(y', y, x)
    """
    @abstractmethod
    def second_order_func(self, yp, y, x):
        """Returns the y'' = f(y', y, x) function
        """
        pass 
    
    @abstractmethod
    def second_order_initial_conditions(self):
        """Returns the initial condition for (y', y, x)
        """
        pass
    
    def first_order_func(self, y, x):
        """Returns function corresponding to the representation of the second order EDO as a first order EDO system"""
        yp = y[:len(y)//2]
        y = y[len(y)//2:]
        return np.array([*yp, *self.second_order_func(yp, y, x)])

    def first_order_initial_conditions(self):
        """Returns initial conditions corresponding to the representation of the second order EDO as a first order EDO system"""
        yp, y, x = self.second_order_initial_conditions()
        return (np.array([y, yp]), x)

class FirstOrderEdoSolver(ABC):
    @abstractmethod
    def advance_to(self, edo: FirstOrderEDO, x_f):
        """Returns the value of the edo at the final x
        """ 
        pass

class SecondOrderEdoSolver(ABC):
    @abstractmethod
    def advance_time(self, edo: SecondOrderEdo, t_final: np.longdouble):
        pass

# class RungeKutta(FirstOrderEdoSolver):
#     def advance_to(self, edo, x_f):
#         pass

# class Example(SecondOrderEdo):
#     """Represents y'' = -y"""

#     def __init__(self, yp0, y0, x0):
#         self.yp0 = yp0
#         self.y0 = y0
#         self.x0 = x0
    
#     def second_order_func(self, yp, y, x):
#         return -y
    
#     def second_order_initial_conditions(self):
#         return np.array([self.yp0, self.y0, self.x0])

# a = Example(0, 1, 1)

# print(a.first_order_initial_conditions())
# print(a.second_order_initial_conditions())

# print(a.first_order_func(np.array([0, 1]), 0))
# print(a.second_order_func(*a.second_order_initial_conditions()))