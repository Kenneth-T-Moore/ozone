import numpy as np

from ozone.api import ODEFunction
from ozone.tests.ode_function_library.two_d_orbit_sys import TwoDOrbitSystem


class TwoDOrbitFunction(ODEFunction):

    def initialize(self):
        self.set_system(TwoDOrbitSystem)
        self.declare_state('position', 'dpos_dt', targets='position', shape=2)
        self.declare_state('velocity', 'dvel_dt', targets='velocity', shape=2)
        self.declare_time(targets='t')

    def get_test_parameters(self):
        ecc = 1. / 2.
        initial_conditions = {
            'position': np.array([1 - ecc, 0]),
            'velocity': np.array([0, np.sqrt((1+ecc) / (1 - ecc))])
        }
        t0 = 0. * np.pi
        t1 = 1. * np.pi
        return initial_conditions, t0, t1

    def get_exact_solution(self, initial_conditions, t0, t):
        ecc = 1 - initial_conditions['position'][0]
        return {'position': np.array([-1 - ecc, 0])}
