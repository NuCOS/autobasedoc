Tutorials
=========

Tutorial 1: Erstes Dokument
---------------------------

Lernen Sie die Grundlagen der PDF-Erstellung:

.. literalinclude:: ../tests/example.py
   :language: python
   :start-after: ## Example prerequisites
   :end-before: ## Example 1
   :caption: Grundkonfiguration

Tutorial 2: Mehrspaltige Layouts
--------------------------------

Erstellen Sie komplexe Layouts:

.. code-block:: python

    # Zweispaltiges Layout
    doc = ar.AutoDocTemplate(
        "multi_column.pdf",
        onLaterPages=(ar.drawLaterLandscape, 2)  # 2 Spalten
    )

Tutorial 3: Header und Footer
----------------------------

Fügen Sie professionelle Kopf- und Fußzeilen hinzu:

.. code-block:: python

    doc.addPageInfo(
        typ="header",
        pos="l", 
        text="Mein Unternehmen"
    )
    
    doc.addPageInfo(
        typ="footer",
        pos="r",
        text="Seite %d" % doc.page,
        addPageNumber=True
    )

Tutorial 4: Matplotlib-Plots
---------------------------

Integrieren Sie Diagramme nahtlos:

.. literalinclude:: ../tests/example.py
   :language: python  
   :start-after: ## Example 2
   :end-before: ## Example 3
   :caption: Plot-Integration