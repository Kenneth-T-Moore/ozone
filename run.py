import numpy as np

from openmdao.api import ExplicitComponent, Problem

from openode.api import ODE, ExplicitTimeMarchingIntegrator, RK4, ForwardEuler


class Comp(ExplicitComponent):

    def initialize(self):
        self.metadata.declare('num', default=1, type_=int)

    def setup(self):
        num = self.metadata['num']

        self.add_input('y', shape=(num, 1))
        self.add_input('t', shape=(num, 1))
        self.add_output('dy_dt', shape=(num, 1))
        self.declare_partials('dy_dt', 'y', dependent=False)

    def compute(self, inputs, outputs):
        outputs['dy_dt'] = np.sin(2*np.pi*inputs['t'])

    def compute_partials(self, inputs, outputs, partials):
        partials['dy_dt', 't'] = 2*np.pi*np.cos(2*np.pi*inputs['t'])


num = 10

ode = ODE(Comp)
ode.declare_state('y', rate_target='dy_dt', state_targets='y')
ode.declare_time('t', 't')

# intgr = ExplicitRelaxedIntegrator(
intgr = ExplicitTimeMarchingIntegrator(
    ode=ode, time_spacing=np.arange(num),
    scheme=RK4(), initial_conditions={'y': 1.}, start_time=0., end_time=1.)

prob = Problem(intgr)
prob.setup()
prob.run_model()
# prob.check_partials(compact_print=True)

print(prob['output_comp.y'])

from openmdao.api import view_model

# view_model(prob)
