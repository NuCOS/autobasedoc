# AutoBaseDoc Tests

Dieses Verzeichnis enthält umfassende Tests und Beispiele für AutoBaseDoc.

## Struktur

```
tests/
├── test_autoreport.py     # Haupttests für autorpt-Modul  
├── example.py             # Grundlegendes Beispiel
├── example_document.py    # Erweiterte Dokumenterstellung
├── document.py            # Document-Wrapper-Klasse
├── flowables.py          # Hilfsfunktionen für Flowables
└── test_*.py             # Spezifische Modultests
```

## Test-Kategorien

### Einheit-Tests (`test_*.py`)
- Modulspezifische Funktionalitätstests
- Automatisierte Validierung
- Kontinuierliche Integration

### Beispiele (`example*.py`) 
- Vollständige Arbeitsabläufe
- Best-Practice-Demonstrationen
- Lernmaterial für Benutzer

### Hilfsbibliotheken (`document.py`, `flowables.py`)
- Wiederverwendbare Komponenten
- Abstraktionsebenen
- Vereinfachte APIs

## Ausführung

```bash
# Alle Tests
python -m pytest tests/

# Spezifische Tests
python tests/test_autoreport.py

# Beispiele
python tests/example.py
```