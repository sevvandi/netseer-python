# Tutorial

---

## Flow

The general flow of processing with Netseer is:

- Load the a time-series list of graphs into Netseer.
- Predict the next graph in the series.

## Getting Started

For this tutorial, I'm defaulting to using [uv](https://docs.astral.sh/uv/getting-started/installation/).
Otherwise set up a python project using pip/venv as standard and create a `main.py`

### Setup

Create a python project:

``` bash
uv init netseer-tutorial
cd netseer-tutorial
```

Add the Netseer package:

``` Python
uv add netseer
```

The tutorial takes place in the `main.py` file.

### Loading

There are two ways to create graphs:

- creating your own list of graphs. Typically this would be a time-series graph.
- randomly generating a list of graphs using Netseer.

If creating your own graphs, Netsser uses the python package `igraph` to handle graphs. Therefore, the created graphs need to be saved in a format that can be used by [`igraph.Graph.Read`](https://python.igraph.org/en/main/api/igraph.Graph.html#Read). For our tutorial we will used GML format graphs.

Save the list of graphs into a directory/folder relative to your project. For example in a /data/ directory.

``` Python

```

For creating a random list of graphs that are growing:

``` Python
from netseer import generate_graph

graph_list = generate_graph.generate_graph_list()
```
