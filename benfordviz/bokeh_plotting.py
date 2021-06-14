from .checks import _check_digit_test_, _check_mantissa_data_
from .bokeh_utils import add_digit_test_figure, add_mantissas_test_figures


class BokehDigitsChart:
    def __init__(self, digit_test):
        self.digit_test = _check_digit_test_(digit_test)
    
    @property
    def figure(self):
        return add_digit_test_figure(self.digit_test)


class BokehMantissasChart:
    def __init__(self, data):
        self.mantissas = _check_mantissa_data_(data)
    
    @property
    def figure(self):
        return add_mantissas_test_figures(self.mantissas)
