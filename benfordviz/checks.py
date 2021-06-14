from numpy import array
from benford import Test, Benford, Mantissas


def _check_digit_test_(digit_test):
    if not isinstance(digit_test, Test):
        raise TypeError(f"This operation accepts only {type(Test)}"
        " instances, which are attributes of the Benford class"
        " in the most recent benford_py API.")
    return digit_test


def _check_mantissa_data_(data):
    if isinstance(data, Benford):
        data.mantisssas()
        return data.Mantissas.data.Mantissa.values
    elif isinstance(data, Mantissas):
        return data.data.Mantissa.values
    elif isinstance(data, array):
        return data
    raise TypeError("This operation accepts one of the following objects as "
        "inputs: benford.Benford, benford.Mantissas, and np.array.")
