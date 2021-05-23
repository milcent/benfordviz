from benford import Test


def _check_digit_test_(digit_test):
    if not isinstance(digit_test, Test):
        raise TypeError(f"This operation accepts only {type(Test)}"
        " instances, which are attributes of the Benford class"
        " in the most recent benford_py API.")
    return digit_test