
import numpy as np
from numbers import Number
from hypothesis import given, strategies
from hypothesis import settings as hyp_settings

from kernelmethods.numeric_kernels import PolyKernel

default_feature_dim = 10
range_feature_dim = [10, 10000]
range_polynomial_degree = [1, 10]

SupportedKernels = (PolyKernel(), )

def gen_random_array(dim):
    """To better control precision and type of floats"""

    return np.random.rand(dim)


@hyp_settings(max_examples=100)
@given(strategies.integers(range_feature_dim[0], range_feature_dim[1]))
def test_kernel_design(sample_dim):
    """
    Every kernel must be
    1. must have a name defined
    2. must be callable with two samples
    3. returns a number

    """

    x = gen_random_array(sample_dim)
    y = gen_random_array(sample_dim)

    for kernel in SupportedKernels:

        if not hasattr(kernel, 'name'):
            raise TypeError('{} does not have name attribute!'.format(kernel))

        try:
            result = kernel(x, y)
        except Exception:
            raise SyntaxError('{} is not callable!'.format(kernel.name))

        if not isinstance(result, Number):
            raise ValueError('result from {} is not a number!'.format(kernel.name))


@hyp_settings(max_examples=1000)
@given(strategies.integers(range_feature_dim[0], range_feature_dim[1]),
       strategies.integers(range_polynomial_degree[0], range_polynomial_degree[1]),
       strategies.floats(min_value=0, max_value=np.Inf,
                         allow_nan=False, allow_infinity=False))
def test_polynomial_kernel(sample_dim, poly_degree, poly_intercept):
    """Tests specific for Polynomial kernel."""

    # TODO input sparse arrays for test
    x = gen_random_array(sample_dim)
    y = gen_random_array(sample_dim)
    poly = PolyKernel(degree=poly_degree, b=poly_intercept)

    try:
        result = poly(x, y)
    except RuntimeWarning:
        raise RuntimeWarning('RunTime warning for:\n'
                             ' x={}\n y={}\n kernel={}\n'.format(x, y, poly))
    except Exception:
        raise Exception('unanticipated exception:\n'
                        ' x={}\n y={}\n kernel={}\n'.format(x, y, poly))

    if not isinstance(result, Number):
        raise ValueError('poly kernel result {} is not a number!\n'
                         'x={}\ny={}\nkernel={}\n'
                         ''.format(result, x, y, poly))
