import numpy as np
import unittest
from itertools import product
from parameterized import parameterized

from ozone.api import ODEIntegrator
from ozone.tests.ode_function_library.simple_homogeneous_func import SimpleHomogeneousODEFunction
from ozone.utils.run_utils import compute_convergence_order, compute_ideal_error
from ozone.methods_list import method_classes, method_families


class Test(unittest.TestCase):

    def setUp(self):
        self.num_times_vector = np.array([10, 15, 20])

        self.ode_function = SimpleHomogeneousODEFunction()

        self.initial_conditions = {'y': 1.}
        self.t0 = 0.
        self.t1 = 1.

        self.state_name = 'y'

        self.formulation = 'solver-based'

    @parameterized.expand(method_classes.keys())
    def test(self, method_name):

        errors_vector, step_sizes_vector, orders_vector, ideal_order = compute_convergence_order(
            self.num_times_vector, self.t0, self.t1, self.state_name,
            self.ode_function, self.formulation, method_name, self.initial_conditions)

        average_order = np.sum(orders_vector) / len(orders_vector)

        self.assertTrue( np.abs(ideal_order - average_order) < 1. )

        print('%18s  %1.1f  %1i  %1.1f'
            % (method_name[:18], average_order, ideal_order, np.abs(ideal_order - average_order)))


if __name__ == '__main__':
    unittest.main()
