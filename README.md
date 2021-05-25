# benfordviz

### Interactive plotting to benford_py.

This is a lib to make interactive plotting of Benford's Law Tests easier.


**Citing**


If you find *`benfordviz`* useful in your research, please consider adding the following citation:

```bibtex
@misc{benfordviz,
      author = {Marcel, Milcent},
      title = {{Benfordviz: a Python Implementation of interactive plotting for Benford's Law Tests}},
      year = {2021},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/milcent/benfordviz}},
}
```
`current version = 0.1.0`

### See [release notes](https://github.com/milcent/benfordviz/releases/) for details of features and bugs.

### Python versions >= 3.6

## Installation

`pip install benfordviz`

### Dependencies

- benford_py >= 0.4.2;
- bokeh >= 2.3.2

### Implemented so far:

- Bokeh
- *More in the furure* - let me know which one you prefer implemented next in the [Issues](https://github.com/milcent/benfordviz/issues). Plotly? Altair?

## Usage

Have your data ingested in a `benford_py` Benford obect like so:

```{Python}
import numpy as np
import benford as bf

# Benford's sets are combinations of random variables
a = np.random.rand(3000)
b = np.random.randint(0,55, 3000)
c = np.random.normal(3000)
abd = a * b * c

bo = bf.Benford(abc)
```

```{Python}
 ########## Benford Object Instantiated ########### 

Initial sample size: 3000.

Test performed on 2941 registries.

Number of discarded entries for each test:
{'F1D': 0, 'F2D': 0, 'F3D': 0, 'SD': 0, 'L2D': 1}
```

Now that you have a Benford object with the main tests already computed, you can give them do `benfordviz` and let it do the rest. The main function for plotting the respective test with `bokeh` is the `bokeh_chart`. It receives a digit test instance, which in turn is an attribute of the Benford object:

- `F1D`: First Digit Test;
- `SD`: Second Digit Test;
- `F2D`: First Two Digits Test;
- `F3D`: First Three Digits Test; and
- `L2D`: Last Two Digits Test.

The `bokeh_chart` function then retuns a `bokeh` `figure`, which you can then give to the output of your choice (browser, file, jupyter...)

```{Python}
from bokeh.plotting import output_notebook, show
from benfordviz import bokeh_chart

output_notebook()
```

```{Python}
#plotting the First Two Digits Test ('F2D')
benf_bokeh_f2d_fig = bokeh_chart(bo.F2D)
show(benf_bokeh_f2d_fig)
```

![First Two Digits Bokeh gif](https://github.com/milcent/benfordviz/blob/main/figures/f2d_bokeh_gif.gif)
