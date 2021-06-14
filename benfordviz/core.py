from .bokeh_plotting import BokehDigitsChart, BokehMantissasChart

def bokeh_digits_chart(digit_test):
    bbc = BokehDigitsChart(digit_test)
    return bbc.figure


def bokeh_mantissas_chart(data):
    bmc = BokehMantissasChart(data)
    return bmc.figure
