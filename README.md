# tx_lege_votes
an analysis of Texas Open State data showing legislators who most vote neither yes or no for bills

Installation:
The conda package ecosystem is utilized heavily by this project. If you don't
yet have conda, you can get a barebones installation with Miniconda.
Instructions are at https://conda.io/miniconda.html

With a conda installation, create an environment with some prerequisites:

```
conda create -n openstate1 python=3.6 bokeh pandas fastparquet python-snappy sqlalchemy mysql-connector-python
```

Not all of our prerequisites are available from the default software channels.
We get a few more things from the conda-forge and ioam organizations on
anaconda.org:

```
conda install -n openstate1 -c ioam -c conda-forge notebook holoviews geoviews datashader
```

Activate this environment, so that the Python environment we've created is the
one we'll use to run the bokeh web app:

```
source activate mapping
```

Download the data from:
```
https://www.dropbox.com/s/xef8tewu9ue6xla/2017-07-01-tx-json.zip?dl=0
```

Extract it into a folder named ``data`` at the same level as main4.py from this
github repo. You don't need to follow this path structure exactly, but if you
don't, you'll need to adjust paths in main4.py.

Running the app
-----------------

Bokeh includes a standalone server. For simplicity and self-containment of this
repository, that's what we'll demonstrate.

In the folder containing main4.py, run

```
bokeh serve .
```

TODO
----
dont know yet

Credits
--------

This app uses the data from https://openstates.org/


```
