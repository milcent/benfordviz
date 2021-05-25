from numpy import array, ceil, log10, sqrt, where

from .constants import FOUND_BAR_COLOR


def _get_upper_lower_bounds(expect_dist, sample_size:int, critical_z:float):
    common_1 = critical_z * (sqrt(expect_dist * (1 - expect_dist) / sample_size))
    common_2 = 1 / (2 * sample_size)
    upper = expect_dist + common_1 + common_2
    lower = expect_dist - common_1 - common_2
    return upper, where(lower > 0, lower, 0)


def _get_in_out_bound_colors_(found, upper, lower, in_colors, out_colors):
    out_bounds = (found > upper) | (found < lower)
    colors = in_colors.copy()
    colors[out_bounds] = out_colors
    return colors


def _set_n_int_places_(array_len:int): return int(ceil(log10(array_len)))


def _get_x_range_(arr): return arr[0] - 1, arr[-1] + 1


def _get_base_bar_colors_(data_len:int, color=FOUND_BAR_COLOR):
    return array([color] * data_len)
