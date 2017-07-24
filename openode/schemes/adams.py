from __future__ import division

import numpy as np
from openode.schemes.scheme import GLMScheme


ab_coeffs = {
    2: np.array([0., 3., -1.]) / 2. ,
    3: np.array([0., 23., -16., 5.]) / 12. ,
    4: np.array([0., 55., -59., 37., -9.]) / 24.,
    5: np.array([0., 1901, -2774., 2616., -1274., 251.]) / 720.,
}


am_coeffs = {
    2: np.array([1., 1.]) / 2. ,
    3: np.array([5., 8., -1.]) / 12. ,
    4: np.array([9., 19., -5., 1.]) / 24. ,
    5: np.array([251., 646., -264., 106., -19.]) / 720.,
}


class Adams(GLMScheme):
    def __init__(self, type_, order):
        assert isinstance(order, int) and 2 <= order <= 5, \
            'For AB or AM, order must be between 2 and 5, inclusive'

        if type_ == 'b':
            num_steps = order
            coeffs = ab_coeffs
        elif type_ == 'm':
            num_steps = order - 1
            coeffs = am_coeffs

        A = np.zeros((1, 1))
        B = np.zeros((num_steps + 1, 1))
        U = np.zeros((1, num_steps + 1))
        V = np.eye(num_steps + 1, k=-1)

        A[0, 0] = coeffs[order][0]
        B[0, 0] = coeffs[order][0]
        B[1, 0] = 1.0
        U[0, 0] = 1.0
        U[0, 1:] = coeffs[order][1:]
        V[0, 0] = 1.0
        V[0, 1:] = coeffs[order][1:]
        V[1, 0] = 0.0

        starting_scheme_name = 'RK4ST'

        starting_coeffs = np.zeros((num_steps + 1, num_steps + 1, 2))
        starting_coeffs[0, -1, 0] = 1.0
        for i in range(num_steps):
            starting_coeffs[i + 1, -i - 1, 1] = 1.0

        starting_time_steps = num_steps

        super(Adams, self).__init__(A=A, B=B, U=U, V=V,
            abscissa=np.ones(1),
            starting_method=(starting_scheme_name, starting_coeffs, starting_time_steps))


class AdamsAlt(GLMScheme):
    def __init__(self, type_, order):
        assert isinstance(order, int) and 2 <= order <= 5, \
            'For AB, order must be between 2 and 5, inclusive'

        if type_ == 'b':
            num_steps = order
            coeffs = ab_coeffs
        elif type_ == 'm':
            num_steps = order - 1
            coeffs = am_coeffs

        A = np.zeros((num_steps + 1, num_steps + 1))
        U = np.zeros((num_steps + 1, num_steps))
        B = np.zeros((num_steps, num_steps + 1))
        V = np.eye(num_steps, k=-1)

        A[-1, :] = coeffs[order][::-1]
        B[0, :] = coeffs[order][::-1]
        V[0, 0] = 1.0
        U[-1, 0] = 1.0
        U[np.arange(num_steps), np.arange(num_steps)[::-1]] = 1.0

        starting_scheme_name = 'RK4'

        starting_coeffs = np.zeros((num_steps, num_steps, 1))
        starting_coeffs[::-1, :, 0] = np.eye(num_steps)

        starting_time_steps = num_steps - 1

        super(AdamsAlt, self).__init__(A=A, B=B, U=U, V=V,
            abscissa=np.linspace(-num_steps + 1, 1, num_steps + 1),
            starting_method=(starting_scheme_name, starting_coeffs, starting_time_steps))


class AB(Adams):
    def __init__(self, order):
        super(AB, self).__init__('b', order)


class AM(Adams):
    def __init__(self, order):
        super(AM, self).__init__('m', order)


class ABalt(AdamsAlt):
    def __init__(self, order):
        super(ABalt, self).__init__('b', order)


class AMalt(AdamsAlt):
    def __init__(self, order):
        super(AMalt, self).__init__('m', order)
