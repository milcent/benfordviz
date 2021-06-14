from .config import get_color_mode

colors = get_color_mode()

FOUND_BAR_COLOR = colors["m"]
OUT_OF_BOUNDS_BAR_COLOR = colors["af"]
EXPECT_LINE_COLOR = colors["s"]
BACKGROUND_COLOR = colors["b"]
EXPECT_BAR_COLOR = colors["t"]
MANTISSAS_EXPECTED_COLOR = colors["m"]
MANTISSAS_FOUND_COLOR = colors["s"]

TOOLTIPS_BASE = [
    # insert ("Digits", f"@{data.index.name}" + "{" + n_int_places * "0" +
    #  "}") in pos 0
    ("Expected", "@Expected{0.0000%}"),
    ("Found", "@Found{0.0000%}"),
    ("Upper Bound", "@upper{0.0000%}"),
    ("Lower Bound", "@lower{0.0000%}")
]
