from benford import Test
from .checks import _check_digit_test_
from .bokeh_utils import add_figure


class BenfordBokehChart:
    def __init__(self, digit_test):
        self.digit_test = _check_digit_test_(digit_test)
    