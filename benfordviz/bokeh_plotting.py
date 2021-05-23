from math import pi
from numpy import array
from bokeh.models import NumeralTickFormatter
from bokeh.models.tools import HoverTool
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure, ColumnDataSource
from benford import Test
from .constants import (EXPECT_LINE_COLOR, EXPECT_BAR_COLOR, FOUND_BAR_COLOR,
                BACKGROUND_COLOR, OUT_OF_BOUNDS_BAR_COLOR , TOOLTIPS_BASE)
from .utils import (_get_in_out_bound_colors_, _get_upper_lower_bounds,
                    _get_x_range_, _set_n_int_places_)


def _add_base_figure_(digits_test, n_int_places):
    max_y = max(digits_test.Found.max(), digits_test.Expected.max())
    fig = figure(
        sizing_mode="stretch_width", x_range=_get_x_range_(digits_test.index),
        y_range=(0, max_y + 10 ** -(n_int_places + 1)),
        title=digits_test.name, x_axis_label="Digits",
        y_axis_label="Found vs. Expected Proportions (%)"
    )
    return fig

def _get_base_bar_colors_(data_len:int, color=FOUND_BAR_COLOR):
    return array([color] * data_len)

def _get_tooltips_(name:str, n_int_places:int,
                   base_tooltips:list=TOOLTIPS_BASE,
                   upper_lower=True):
    tooltips = base_tooltips.copy()
    digit_tooltip = ("Digits", f"@{name}" + "{" + n_int_places * "0" + "}")
    tooltips.insert(0, digit_tooltip)
    if not upper_lower:
        tooltips  = tooltips[:-2]
    return tooltips

def _add_glyphs_(fig, data, confidence=None):
    
    source = ColumnDataSource(data)
    name = data.index.name

    fig.line(x=name, y="Expected", width=2, legend_label="Expected",
             source=source, color=EXPECT_LINE_COLOR, level="overlay")

    source.data["colors"] = _get_base_bar_colors_(len(data))

    if not confidence:
        fig.vbar(x=name, top="Found", width=.75, color="colors",
                 source=source, legend_label="Found")
        tooltips = _get_tooltips_(name, _set_n_int_places_(len(data)),
                                  upper_lower=False)
        fig.add_tools(HoverTool(tooltips=tooltips, mode="vline"))
        return fig

    source.data["upper"], source.data["lower"] = _get_upper_lower_bounds(
        data.Expected.values, data.N, data.critical_values["Z"]
    )
    source.data["colors"] = _get_in_out_bound_colors_(
        data.Found.values, source.data["upper"], source.data["lower"],
        source.data["colors"], OUT_OF_BOUNDS_BAR_COLOR
    )
    fig.vbar(x=name, top="Found", width=.75, legend_label="Found",
             color="colors", source=source)
    fig.varea(x=name, y1="lower", y2="upper", fill_alpha=.4, level="underlay",
              source=source, fill_color=EXPECT_LINE_COLOR,
              legend_label="Confidence Bounds")
    tooltips = _get_tooltips_(name, _set_n_int_places_(len(data)))
    fig.add_tools(HoverTool(tooltips=tooltips, mode="vline"))
    return fig

def _add_figure_specs_(fig, x_ticks, n_int_places:int):
    fig.xaxis.ticker = FixedTicker(ticks=x_ticks)
    fig.xaxis.major_label_orientation = pi / 2
    fig.xgrid.visible, fig.ygrid.visible = False, False
    fig.xaxis[0].formatter = NumeralTickFormatter(format="0" * n_int_places)
    fig.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    fig.background_fill_color = BACKGROUND_COLOR
    fig.legend.background_fill_color = BACKGROUND_COLOR
    fig.legend.border_line_color = BACKGROUND_COLOR
    fig.legend.click_policy = "hide"
    return fig

class BenfordBokehChart():
    def __init__(self, digit_test):
        if not isinstance(digit_test, Test):
            raise TypeError(f"{self.__name__} accepts only {type(Test)}"
                " instances, which are attributes of the Benford classe"
                " in the most recent benford_py API.")
        self.digit_test = digit_test
        self.n_int_places = _set_n_int_places_(len(self.digit_test))

    