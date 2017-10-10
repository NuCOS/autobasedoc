.. _installation:

Install
=======

Simple
------

.. index:: Install

If you want it simple, go to a console an type:

.. code-block:: python

    pip install autobasedoc

With virtualenv
---------------

Otherwise it may also be recommended to install it into a virtual environment. To that end type in a console:

.. code-block:: python

    virtualenv venv
    source ./venv/bin/activate
    pip install autobasedoc

Using Miniconda/Anaconda
------------------------

I prefer miniconda but the package does not exist for conda, yet:

.. code-block:: python

    conda create -n abd-env

    source activate abd-env

    pip install autobasedoc

Python Compatibility
--------------------

The module is compatible with Python 3.4/3.5/3.6 It should also work in any other Python Version but not yet tested.

Platforms
---------

The module is platform independent. Up to now it is tested on linux (ubuntu). Other platforms will follow (at lease Windows 10 should always work).
