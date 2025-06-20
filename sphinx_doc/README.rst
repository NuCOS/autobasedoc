AutoBaseDoc - Professionelle PDF-Automatisierung
================================================

AutoBaseDoc ist eine Python-Bibliothek für die automatisierte Erstellung 
professioneller PDF-Dokumente mit erweiterten Layout-Funktionen.

Hauptfeatures
------------

🎨 **Flexible Layouts**
   - Portrait- und Landscape-Formate
   - Mehrspaltige Designs  
   - Automatische Frame-Verwaltung

📊 **Matplotlib-Integration**
   - Nahtlose Plot-Einbettung
   - Automatische Bildgrößenanpassung
   - Konsistente Schriftarten

📑 **Automatische Navigation**
   - Inhaltsverzeichnisse mit Links
   - PDF-Bookmarks
   - Seitenreferenzen

✨ **Styling-System**
   - Vordefinierte Stile
   - TTF-Font-Unterstützung
   - Farbmanagement

Schnellstart
-----------

.. code-block:: python

    import autobasedoc.autorpt as ar
    
    # Dokument erstellen
    doc = ar.AutoDocTemplate("report.pdf")
    styles = ar.Styles()
    
    # Inhalt hinzufügen
    content = []
    content.append(ar.Paragraph("Mein Titel", styles.title))
    
    # PDF generieren
    doc.multiBuild(content)

Architektur
----------

Das Paket besteht aus mehreren Modulen:

- ``autorpt``: Kern-Dokumentfunktionalität
- ``autoplot``: Matplotlib-Integration  
- ``styles``: Styling-System
- ``pageinfo``: Seiteninformationen
- ``fonts``: Font-Management