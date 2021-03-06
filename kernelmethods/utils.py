
import numpy as np
from scipy.sparse import issparse
from kernelmethods import config
from collections.abc import Iterable

def check_input_arrays(x, y, ensure_dtype=np.number):
    """
    Ensures the inputs are
    1) 1D arrays (not matrices)
    2) with compatible size
    3) of a particular data type
    and hence are safe to operate on.

    Parameters
    ----------
    x : iterable

    y : iterable

    ensure_dtype : dtype

    Returns
    -------
    x : ndarray

    y : ndarray

    """

    x = ensure_ndarray_1D(x, ensure_dtype)
    y = ensure_ndarray_1D(y, ensure_dtype)

    if x.size != y.size:
        raise ValueError('x (n={}) and y (n={}) differ in size! '
                         'They must be of same length'.format(x.size, y.size))

    return x, y


def ensure_ndarray_2D(array, ensure_dtype=np.number, ensure_num_cols=None):
    """Converts the input to a numpy array and ensure it is 1D."""

    if not isinstance(array, np.ndarray):
        array = np.asarray(array)

    # squeezing only 3rd dim if they are singleton, leaving 1st & 2nd dim alone
    axes_to_sqz = tuple(ax for ax, sz in enumerate(array.shape) if sz==1 and ax>1)
    array = np.squeeze(array, axis=axes_to_sqz)

    array = ensure_ndarray_size(array, ensure_dtype=ensure_dtype, ensure_num_dim=2)

    if ensure_num_cols is not None and array.shape[1] != ensure_num_cols:
        raise ValueError('The number of columns differ from expected {}'
                         ''.format(ensure_num_cols))

    return array


def ensure_ndarray_1D(array, ensure_dtype=np.number):
    """Converts the input to a numpy array and ensure it is 1D."""

    if not isinstance(array, np.ndarray):
        array = np.asarray(array)

    # squeezing only 2nd, 3rd dim if they are singleton, leaving 1st dim alone
    axes_to_sqz = tuple(ax for ax, sz in enumerate(array.shape) if sz==1 and ax>0)
    array = np.squeeze(array, axis=axes_to_sqz)

    return ensure_ndarray_size(array, ensure_dtype=ensure_dtype, ensure_num_dim=1)


def ensure_ndarray_size(array, ensure_dtype=np.number, ensure_num_dim=1):
    """Converts the input to a numpy array and ensure it is of specified dim."""

    if array.ndim != ensure_num_dim:
        raise ValueError('array must be {}-dimensional! '
                         'It has {} dims with shape {} '
                         ''.format(ensure_num_dim, array.ndim, array.shape))

    if not np.issubdtype(ensure_dtype, array.dtype):
        prev_dtype = array.dtype
        try:
            array = array.astype(ensure_dtype)
        except:
            raise ValueError('Unable to recast input dtype from {} to required {}!'
                             ''.format(prev_dtype, ensure_dtype))

    return array


def check_callable(input_func, min_num_args=2):
    """Ensures the input func 1) is callable, and 2) can accept a min # of args"""

    if not callable(input_func):
        raise TypeError('Input function must be callable!')

    from inspect import signature
    # would not work for C/builtin functions such as numpy.dot
    func_signature = signature(input_func)

    if len(func_signature.parameters) < min_num_args:
        raise TypeError('Input func must accept atleast {} inputs'.format(min_num_args))

    return input_func


def get_callable_name(input_func, name=None):
    """Returns the callable name"""

    if name is None:
        if hasattr(input_func, '__name__'):
            return input_func.__name__
        else:
            return ''
    else:
        return str(name)

_float_eps = np.finfo('float').eps

def _ensure_min_eps(x):
    return  np.maximum(_float_eps, x)

def not_symmetric(matrix):
    """Returns true if the input matrix is not symmetric."""

    if not np.isclose(matrix, matrix.T).all():
        return True
    else:
        return False

def check_operation_kernel_matrix(operation):
    """Validates whether input is a valid operation on KernelMatrices"""

    opr = operation.lower()
    if opr not in config.VALID_KERNEL_MATRIX_OPS:
        raise ValueError('Invalid kernel matrix operation - must be one of:\n{}'
                         ''.format(config.VALID_KERNEL_MATRIX_OPS))

    return opr


def min_max_scale(array):
    """Rescale the array values from 0 to 1 via min-max normalization."""

    array = np.array(array)
    min_val = array.min()
    return (array - min_val) / (np.max(array) - min_val)


def contains_nan_inf(matrix):
    """
    Helper func to check for the presence of NaN or Inf.

    Returns True if any element is not finite (Inf) or NaN. Returns False otherwise.

    This is designed to works for both dense and sparse matrices!
    """

    if issparse(matrix):
        matrix = matrix.todense()

    if (not np.isfinite(matrix).all()) \
        or (np.isnan(matrix).any()):
        return True
    else:
        return False


def is_iterable_but_not_str(input_obj, min_length=1):
    """Boolean check for iterables that are not strings and of a minimum length"""

    if not (not isinstance(input_obj, str) and isinstance(input_obj, Iterable)):
        return False

    if len(input_obj) < min_length:
        return False
    else:
        return True
