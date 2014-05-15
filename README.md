progressbar
===========

Python progress bar project with support for HTML5 in the IPython Notebook.

![Demo](Demo/Demo.gif?raw=true "Demo")

Two progress bar implementations are provided, one using ASCII and one using HTML/CSS/Javascript.  Perhaps at some point these can be amalagamated into a single object that displays HTML in notebook and ASCII in a terminal/qt.

The Rich one is implemented by inserting an HTML5 `progress` element into the notebook and manipulated with Javascript.

A class that wraps an iterable/iterator, `ProgIter` is provided for use in monitoring for loop progress.


