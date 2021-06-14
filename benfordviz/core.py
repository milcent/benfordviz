from .bokeh_plotting import BokehDigitsChart, BokehMantissasChart

def bokeh_digits_chart(digit_test):
    """Creates a bokeh chart of the Benford Digit Test provided

    Args:
        digit_test (benford.Test): Digit Test (F1D: First Digit;
            SD: Second Digit; F2D: First Two Digits; F3D: First Three
            Digits; and L2D: Last Tow Digits). All can be found as
            attributes of the Benford instance.

    Returns:
        bokeh.Figure: Digit Test figure to be displayed. Still needs to be
            fed to the bokeh show function, which will render the plot
            according to the output chosen. 
    """
    bbc = BokehDigitsChart(digit_test)
    return bbc.figure


def bokeh_mantissas_chart(mant_data):
    """Creates a bokeh chart of the Benford Mantissas Test provided

    Args:
        mant_data: Mantissas distributions. May be an numpy.ndarray, a pandas
            Series, a benford.Mantissas instance, or a benford.Benford
            instance.

    Returns:
        bokeh.Figure: Mantissas Test figure to be displayed. Still needs
            to be fed to the bokeh show function, which will render the plot
            according to the output chosen. 
    """
    bmc = BokehMantissasChart(mant_data)
    return bmc.figure
