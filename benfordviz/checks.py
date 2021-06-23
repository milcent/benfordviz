from numpy import ndarray
from pandas import Series

from benford import Test, Benford, Mantissas


def _check_digit_test_(digit_test):
    if not isinstance(digit_test, Test):
        raise TypeError(f"This operation accepts only {type(Test)}"
        " instances, which are attributes of the Benford class"
        " in the most recent benford_py API.")
    return digit_test


def _check_mantissa_data_(mant_data):
    if isinstance(mant_data, ndarray):
        return mant_data
    elif isinstance(mant_data, Benford):
        if not hasattr(mant_data, "Mantissas"):
            mant_data.mantissas()
        return mant_data.Mantissas.data.Mantissa.values
    elif isinstance(mant_data, Mantissas):
        return mant_data.data.Mantissa.values
    elif isinstance(mant_data, Series):
        return mant_data.values
    raise TypeError("This operation accepts one of the following objects as "
        "inputs: benford.Benford, benford.Mantissas, and np.array.")
