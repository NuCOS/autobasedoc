Examples
========

An example should always describe the full workflow, here a very basic example on the usage:

Prerequisites
-------------

There are some preparations to make before you can actually add content to the document.

.. literalinclude:: ../tests/example.py
   :language: python
   :start-after: ## Example prerequisites
   :end-before: ## Example 1

A simple Table
--------------

Adding a simple Table using just the normal way to do this with reportlab.

 .. literalinclude:: ../tests/example.py
    :language: python
    :start-after: ## Example 1
    :end-before: ## Example 2

A simple Matplotlib Plot
------------------------

You can use a decorator `@ap.autoPdfImg` from the autoplot module to turn a simple plot function into a reportlab flowable.

 .. literalinclude:: ../tests/example.py
    :language: python
    :start-after: ## Example 2
    :end-before: ## Example 3


A simple Matplotlib Plot and a Legend
-------------------------------------

If you want to have a separate Legend that you can separately add to your document you can use the decorator `@ap.autoPdfImage`.

 .. literalinclude:: ../tests/example.py
    :language: python
    :start-after: ## Example 3
    :end-before: ## Finally

Building the contents
---------------------

Finally build the whole document.

.. literalinclude:: ../tests/example.py
   :language: python
   :start-after: ## Finally
