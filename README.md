# Netseer

## Predicting graph structure from a time series of graphs

---

This is a Python implementation of [Netseer](https://arxiv.org/html/2401.04280v1)
Documentation: [GitHub](https://sevvandi.github.io/netseer-python)

## Purpose

Netseer is a tool that outputs a predicted graph based on a time series graph sequence.

Citing:

```
Sevvandi Kandanaarachchi, Ziqi Xu, Stefan Westerlund, and Conrad Sanderson. 2025. “Predicting Graph Structure via Adapted Flux Balance Analysis.” [https://arxiv.org/abs/2507.05806](https://arxiv.org/abs/2507.05806).
```

## Installation

This package is available on PyPI, and can be installed with PIP or with a Package Manager:

``` Bash
pip install netseer # or
uv add netseer
```

## Quick Example

Generating an example list of graphs:

``` Python
from netseer import generate_graph, prediction

graph_list = generate_graph.generate_graph_list()
```

Note: `generate_graph_list()` has parameters to tailor the created graphs.
See the Reference section in the documentation for more.

Predicting on that graph list:

``` Python
predict = prediction.predict_graph(graph_list, h=1)
```

Increasing the `h` parameter increases how much into the future the prediction is, with `h=1` being 1 step in the graph sequence.
