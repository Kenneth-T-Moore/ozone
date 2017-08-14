import numpy as np
from six import iteritems
import scipy.sparse

from openmdao.utils.options_dictionary import OptionsDictionary

from openmdao.api import ExplicitComponent


class TimeComp(ExplicitComponent):

    def initialize(self):
        self.metadata.declare('time_units', type_=(str, type(None)), required=True)
        self.metadata.declare('normalized_times', type_=np.ndarray, required=True)
        self.metadata.declare('stage_norm_times', type_=np.ndarray, required=True)

    def setup(self):
        time_units = self.metadata['time_units']
        normalized_times = self.metadata['normalized_times']
        stage_norm_times = self.metadata['stage_norm_times']

        num_time_steps = len(normalized_times)
        num_stage_times = len(stage_norm_times)
        num_h_vec = num_time_steps - 1

        self.add_input('initial_time', units=time_units)
        self.add_input('final_time', units=time_units)
        self.add_output('h_vec', shape=num_h_vec, units=time_units)
        self.add_output('stage_times', shape=num_stage_times, units=time_units)

        self.declare_partials('h_vec', 'initial_time',
            val=normalized_times[:-1] - normalized_times[1:])
        self.declare_partials('h_vec', 'final_time',
            val=normalized_times[1:] - normalized_times[:-1])

        val = stage_norm_times
        self.declare_partials('stage_times', 'initial_time', val=np.array(1 - stage_norm_times))
        self.declare_partials('stage_times', 'final_time', val=np.array(stage_norm_times))

    def compute(self, inputs, outputs):
        normalized_times = self.metadata['normalized_times']
        stage_norm_times = self.metadata['stage_norm_times']

        t0 = inputs['initial_time']
        t1 = inputs['final_time']

        outputs['h_vec'] = (normalized_times[1:] - normalized_times[:-1]) * (t1 - t0)
        outputs['stage_times'] = t0 + stage_norm_times * (t1 - t0)