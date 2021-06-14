from numpy import array, ceil, cos, log10, linspace, pi, sin, sqrt, where
from pandas import concat, DataFrame

from .constants import (FOUND_BAR_COLOR, MANTISSAS_EXPECTED_COLOR,
    MANTISSAS_FOUND_COLOR)


def _get_upper_lower_bounds(expect_dist, sample_size:int, critical_z:float):
    """Generates the upper and lower bounds values for the Digits Tests plots
    according to the expected distribution, sample size and critical Z score
    """
    common_1 = critical_z * (sqrt(expect_dist * (1 - expect_dist) / sample_size))
    common_2 = 1 / (2 * sample_size)
    upper = expect_dist + common_1 + common_2
    lower = expect_dist - common_1 - common_2
    return upper, where(lower > 0, lower, 0)


def _get_in_out_bound_colors_(found, upper, lower, in_colors, out_colors):
    """Array of colors dependent on whether the values fall in or out of the
    boundaries 
    """
    out_bounds = (found > upper) | (found < lower)
    colors = in_colors.copy()
    colors[out_bounds] = out_colors
    return colors


def _set_n_int_places_(array_len:int):
    """Computes the number of integer places of the digits, dependent on the
    digits set size - used in the ticks labels
    """
    return int(ceil(log10(array_len)))


def _get_x_range_(arr): return arr[0] - 1, arr[-1] + 1


def _get_base_bar_colors_(data_len:int, color=FOUND_BAR_COLOR):
    return array([color] * data_len)


def _get_expected_found_mantissas_df_(mant_dist):
    """Creates a dataframe with the found and the expected mantissas 
    """
    mant_dist.sort()
    expecetd = linspace(0, .99999999, len(mant_dist))
    return DataFrame({"Expected": expecetd, "Mantissas": mant_dist})


def _get_mantissas_arc_plot_df_(mantissas):
    """Creates a data frame with the values to be used in the Mantissas
    Arc Plot and the colors to be used. The last row holds the means and
    the color to be used in the gravity center.
    """
    x = cos(2 * pi * mantissas)
    y = sin(2 * pi * mantissas)
    
    arc_df = DataFrame({"arc_x": x, "arc_y": y}).append(
                {"arc_x": x.mean(), "arc_y": y.mean()}, ignore_index=True)\
                .assign(colors=MANTISSAS_EXPECTED_COLOR)

    arc_df.iloc[-1, 2] = MANTISSAS_FOUND_COLOR
    
    return arc_df