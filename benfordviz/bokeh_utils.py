from math import pi
from bokeh.models import NumeralTickFormatter, Label
from bokeh.models.tools import HoverTool
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import row

from .constants import (EXPECT_LINE_COLOR, BACKGROUND_COLOR, TOOLTIPS_BASE,
    OUT_OF_BOUNDS_BAR_COLOR, MANTISSAS_EXPECTED_COLOR, MANTISSAS_FOUND_COLOR)
from .utils import (_get_in_out_bound_colors_, _get_upper_lower_bounds,
    _get_x_range_, _set_n_int_places_, _get_base_bar_colors_,
    _get_expected_found_mantissas_df_, _get_mantissas_arc_plot_df_)


def _get_tooltips_(name:str, n_int_places:int,
                   base_tooltips:list=TOOLTIPS_BASE,
                   upper_lower=True):
    """Selectes the tooltips list based of the Digits Test provided and the
    presence or not of lower and upper bounds to values to show
    """
    tooltips = base_tooltips.copy()
    digit_tooltip = ("Digits", f"@{name}" + "{" + n_int_places * "0" + "}")
    tooltips.insert(0, digit_tooltip)
    if not upper_lower:
        tooltips  = tooltips[:-2]
    return tooltips

# LOOONG function! Could be broken into at least three, but did not see 
# the need for separation
def add_digit_test_figure(digit_test):
    """Builds the Digits Test Figure, based on the digits test provided

    Args:
        digit_test (benford.Test): instance of digit test

    Returns:
        bokeh.Figure: figure to be displayed
    """
            
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


def _ordered_mantissas_plot_(mant_dist):
    """Creates the Ordered Mantissas plot

    Args:
        mant_dist (numpy.ndarray): array with the mantissas distribution

    Returns:
        bokeh.Figure: figure to be displayed
    """
    source = ColumnDataSource(_get_expected_found_mantissas_df_(mant_dist))
    fig = figure(
        title="Ordered Mantissas Plot", x_range=(0,1),
        y_range=(0, 1), aspect_ratio=1.0, sizing_mode="scale_both"
    )
    fig.line(x="Expected", y="Expected", width=2, legend_label="Expected",
             color=MANTISSAS_EXPECTED_COLOR, source=source)

    fig.line(x="Expected", y="Mantissas", width=3, legend_label="Mantissas",
             line_dash="dashed", color=MANTISSAS_FOUND_COLOR, source=source)

    fig.add_tools(HoverTool(tooltips=[
                    ("Expected", "@Expected{0.0000}"),
                    ("Mantissa", "@Mantissas{0.0000}")
                    ])
                )
    
    fig.xgrid.visible, fig.ygrid.visible = False, False
    fig.background_fill_color = BACKGROUND_COLOR
    fig.legend.background_fill_color = None
    fig.legend.location = "top_left"
    fig.legend.border_line_color = None
    fig.legend.click_policy = "hide"

    return fig


def _mantissas_arc_plot_(mant_dist):
    """Creates the Mantissa Arc Plot

    Args:
        mant_dist (numpy.ndarray): array with Mantissas distribution

    Returns:
        bokeh.Figure: figure to be displayed
    """
    arc_df = _get_mantissas_arc_plot_df_(mant_dist)

    gc_coords = {
        "x": arc_df.arc_x.iloc[-1] - 0.05,
        "y": arc_df.arc_y.iloc[-1] - 0.1
    }

    source = ColumnDataSource(arc_df)

    fig = figure(
        title="Mantissas Arc Plot", x_range=(-1.1, 1.1),
        y_range=(-1.1, 1.1), aspect_ratio=1.0, sizing_mode="scale_both",
        x_axis_label="cos(2.П.mantissas)", y_axis_label="sin(2.П.mantissas)",
        tooltips=[
                    ("X_coord", "@arc_x{0.0000}"),
                    ("Y_coord", "@arc_y{0.0000}")
                    ]
    )

    fig.scatter(x="arc_x", y="arc_y", color="colors", source=source)

    grav_center_annot = Label(
        x=gc_coords["x"], y=gc_coords["y"],
        text=f"Gravity Center",text_align="right", text_font_size="14px"
    )

    fig.add_layout(grav_center_annot)

    fig.background_fill_color = BACKGROUND_COLOR

    return fig


def add_mantissas_test_figures(mant_dist):
    """Joins the Mantissas (Ordered and Arc) plots

    Args:
        mant_dist (numpy.ndarray): array with Mantissas distributions

    Returns:
        bokeh.Row: figure with the two plots figures to be displayed
    """
    ordered_mant_fig = _ordered_mantissas_plot_(mant_dist)
    mant_arc_fig = _mantissas_arc_plot_(mant_dist)
    return row(ordered_mant_fig, mant_arc_fig)
