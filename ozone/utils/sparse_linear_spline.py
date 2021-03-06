import numpy as np


def get_sparse_linear_spline(in_vec, out_vec):
    if np.max(out_vec) > in_vec[-1] + 1e-16 or np.min(out_vec) < in_vec[0] - 1e-16:
        raise Exception('Internal error: cannot extrapolate using sparse linear spline')

    num_in = len(in_vec)
    num_out = len(out_vec)

    iright = np.maximum(1, np.searchsorted(in_vec, out_vec, side='left'))
    ileft = iright - 1

    w = (out_vec - in_vec[ileft]) / (in_vec[iright] - in_vec[ileft])

    data = np.zeros((num_out, 2))
    rows = np.zeros((num_out, 2), int)
    cols = np.zeros((num_out, 2), int)

    data[:, 0] = 1 - w
    data[:, 1] = w
    rows[:, 0] = np.arange(num_out)
    rows[:, 1] = np.arange(num_out)
    cols[:, 0] = ileft
    cols[:, 1] = iright

    return data.flatten(), rows.flatten(), cols.flatten()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import scipy.sparse

    num_in = 3
    num_out = 1000
    in_x = np.linspace(0, 10, num_in)
    in_y = in_x ** 2
    out_x = np.linspace(0, 10, num_out)
    out_y = None

    data, rows, cols = get_sparse_linear_spline(in_x, out_x)
    mtx = scipy.sparse.csc_matrix((data, (rows, cols)))
    out_y = mtx.dot(in_y)

    plt.plot(in_x, in_y, 'o')
    plt.plot(out_x, out_y)
    plt.show()
