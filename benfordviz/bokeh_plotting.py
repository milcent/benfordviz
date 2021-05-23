from benford import Test
from .bokeh_utils import (_add_base_figure_, _add_figure_specs_, _add_glyphs_,
                          _get_tooltips_)


class BenfordBokehChart:
    def __init__(self, digit_test):
        if not isinstance(digit_test, Test):
            raise TypeError(f"{self.__name__} accepts only {type(Test)}"
                " instances, which are attributes of the Benford class"
                " in the most recent benford_py API.")
        self.digit_test = digit_test
    