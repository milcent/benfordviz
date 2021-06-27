from .bokeh_utils import add_digit_test_figure, add_mantissas_test_figures
from .checks import _check_digit_test_, _check_mantissa_data_


class BokehDigitsChart:
    """Holds the Benford Digit Test and generates is respective bokeh
    chart.

    Args:
        digit_test (benford.Test): Benford Digit Test to be displayed
    """

    def __init__(self, digit_test):
        self.digit_test = _check_digit_test_(digit_test)
    
    @property
    def figure(self):
        return add_digit_test_figure(self.digit_test)


class BokehMantissasChart:
    """Holds the Benford Mantissas Test and generates is respective bokeh
    chart.

    Args:
        mant_data : Mantissas data. May be a numpy.ndarray, a pandas Series,
            a benford.Benford instance, or a benford.Mantissas instance
    """
    
    def __init__(self, mant_data):
        self.mantissas = _check_mantissa_data_(mant_data)
    
    @property
    def figure(self):
        return add_mantissas_test_figures(self.mantissas)
