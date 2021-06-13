from benford import Test
from .checks import _check_digit_test_
from .bokeh_utils import add_digit_test_figure


class BenfordBokehChart:
    def __init__(self, digit_test):
        self.digit_test = _check_digit_test_(digit_test)
    
    @property
    def figure(self):
        return add_digit_test_figure(self.digit_test)