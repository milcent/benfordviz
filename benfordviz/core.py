from .bokeh_plotting import BenfordBokehChart

def bokeh_chart(digit_test):
    bbc = BenfordBokehChart(digit_test)
    return bbc.figure