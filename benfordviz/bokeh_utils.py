from math import pi
from numpy import array
from bokeh.models import NumeralTickFormatter
from bokeh.models.tools import HoverTool
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure, ColumnDataSource
from benford import Test
from .constants import (EXPECT_LINE_COLOR, BACKGROUND_COLOR,
                        OUT_OF_BOUNDS_BAR_COLOR , TOOLTIPS_BASE)
from .utils import (_get_in_out_bound_colors_, _get_upper_lower_bounds,
                    _get_x_range_, _set_n_int_places_, _get_base_bar_colors_)


def _get_tooltips_(name:str, n_int_places:int,
                   base_tooltips:list=TOOLTIPS_BASE,
                   upper_lower=True):
    tooltips = base_tooltips.copy()
    digit_tooltip = ("Digits", f"@{name}" + "{" + n_int_places * "0" + "}")
    tooltips.insert(0, digit_tooltip)
    if not upper_lower:
        tooltips  = tooltips[:-2]
    return tooltips

# LOOONG function! Could be broken into at least three, but did not see 
# the need for separation
def add_figure(digit_test):

    max_y = max(digit_test.Found.max(), digit_test.Expected.max())
    len_dig = len(digit_test)
    n_int_places = _set_n_int_places_(len_dig)
    ratio = 3.2 if len_dig == 100 else 2.1

    fig = figure(
        title=digit_test.name, x_range=_get_x_range_(digit_test.index),
        y_range=(0, max_y + 10 ** -(n_int_places + 1)), aspect_ratio=ratio,
        sizing_mode="scale_both", x_axis_label="Digits",
        y_axis_label="Found vs. Expected Proportions (%)"
    )
    source = ColumnDataSource(digit_test)
    name = digit_test.index.name

    fig.line(x=name, y="Expected", width=2, legend_label="Expected",
             source=source, color=EXPECT_LINE_COLOR, level="overlay")

    source.data["colors"] = _get_base_bar_colors_(len_dig)

    if not digit_test.critical_values["Z"]:
        fig.vbar(x=name, top="Found", width=.75, color="colors",
                 source=source, legend_label="Found")
        tooltips = _get_tooltips_(name, n_int_places, upper_lower=False)
        fig.add_tools(HoverTool(tooltips=tooltips, mode="vline"))
    else:
        source.data["upper"], source.data["lower"] = _get_upper_lower_bounds(
            digit_test.Expected.values, digit_test.N,
            digit_test.critical_values["Z"]
        )
        source.data["colors"] = _get_in_out_bound_colors_(
            digit_test.Found.values, source.data["upper"], source.data["lower"],
            source.data["colors"], OUT_OF_BOUNDS_BAR_COLOR
        )
        fig.vbar(x=name, top="Found", width=.75, legend_label="Found",
                color="colors", source=source)
        fig.varea(x=name, y1="lower", y2="upper", fill_alpha=.4, level="underlay",
                source=source, fill_color=EXPECT_LINE_COLOR,
                legend_label=f"{digit_test.confidence}% Confidence Bounds")
        tooltips = _get_tooltips_(name, n_int_places)
        fig.add_tools(HoverTool(tooltips=tooltips, mode="vline"))
 
    fig.xaxis.ticker = FixedTicker(ticks=digit_test.index.values)
    fig.xaxis.major_label_orientation = pi / 2
    fig.xgrid.visible, fig.ygrid.visible = False, False
    fig.xaxis[0].formatter = NumeralTickFormatter(format="0" * n_int_places)
    fig.yaxis[0].formatter = NumeralTickFormatter(format="0.0%")
    fig.background_fill_color = BACKGROUND_COLOR
    fig.legend.background_fill_color = None
    fig.legend.border_line_color = None
    fig.legend.click_policy = "hide"
    
    return fig
