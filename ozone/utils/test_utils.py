import numpy as np
import unittest
from six import iteritems

import matplotlib
matplotlib.use('Agg')

from ozone.api import ODEIntegrator
from ozone.utils.run_utils import run_integration


class OzoneODETestCase(unittest.TestCase):

    def run_error_test(self):
        from openmdao.api import Problem

        num_times = 100
        method_name = 'RK4'
        formulation = 'solver-based'

        ode_function = self.ode_function_class()
        initial_conditions, t0, t1 = ode_function.get_test_parameters()

        runtime, errors = run_integration(
            num_times, t0, t1, initial_conditions, ode_function, formulation, method_name)

        for key in errors:
            self.assertTrue(errors[key] < 1e-2)

    def run_partials_test(self):
        from openmdao.api import Problem

        ode_function = self.ode_function_class()
        initial_conditions, t0, t1 = ode_function.get_test_parameters()
        exact_solution = ode_function.get_exact_solution(initial_conditions, t0, t1)

        num = 10

        times = np.linspace(t0, t1, num)

        method_name = 'ImplicitMidpoint'
        formulation = 'solver-based'

        integrator = ODEIntegrator(ode_function, formulation, method_name,
            times=times, initial_conditions=initial_conditions,
        )

        prob = Problem(integrator)
        prob.setup()
        prob.run_model()

        jac = prob.check_partials(compact_print=True)
        for comp_name, jac_comp in iteritems(jac):
            for partial_name, jac_partial in iteritems(jac_comp):
                mag_fd = jac_partial['magnitude'].fd
                mag_fwd = jac_partial['magnitude'].forward
                mag_rev = jac_partial['magnitude'].reverse

                abs_fwd = jac_partial['abs error'].forward
                abs_rev = jac_partial['abs error'].reverse

                rel_fwd = jac_partial['rel error'].forward
                rel_rev = jac_partial['rel error'].reverse

                non_zero = np.max([mag_fd, mag_fwd, mag_rev]) > 1e-12
                if non_zero:
                    self.assertTrue(rel_fwd < 1e-3 or abs_fwd < 1e-3)
                    self.assertTrue(rel_rev < 1e-3 or abs_rev < 1e-3)
