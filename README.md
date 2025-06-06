# AutoBaseDoc - Professional PDF Automation

> Automated creation of professional PDF documents with advanced layout features using ReportLab and Matplotlib integration.

![Documentation Status](https://readthedocs.org/projects/autobasedoc/badge/?version=latest)
![Current Version PyPI](https://img.shields.io/pypi/v/autobasedoc.svg)
![Python Version](https://img.shields.io/pypi/pyversions/autobasedoc.svg)
![License](https://img.shields.io/github/license/NuCOS/autobasedoc.svg)

AutoBaseDoc is a Python library that extends ReportLab's capabilities to provide automated PDF document generation with sophisticated layout management, matplotlib integration, and professional styling. It's designed for creating reports, documentation, and complex multi-page documents with minimal code.

## ✨ Key Features

### 🎨 **Flexible Layout System**
- **Portrait and Landscape**: Seamless switching between orientations
- **Multi-column Layouts**: Configurable column structures with automatic flow
- **Frame Management**: Advanced frame handling with automatic sizing
- **Mixed Formats**: Combine different layouts within a single document

### 📊 **Matplotlib Integration**
- **Direct Plot Embedding**: Convert matplotlib figures to PDF flowables
- **Automatic Scaling**: Intelligent image resizing to fit frames
- **Vector Graphics**: Preserve plot quality with PDF vector support
- **Consistent Styling**: Unified font and color management

### 📑 **Automatic Navigation**
- **Table of Contents**: Auto-generated with clickable links
- **PDF Bookmarks**: Hierarchical navigation structure
- **Cross-references**: Internal document linking
- **Page Numbering**: Flexible header/footer management

### ✨ **Professional Styling**
- **Predefined Styles**: Ready-to-use paragraph and heading styles
- **Custom Fonts**: TTF font support with automatic registration
- **Color Management**: Consistent color schemes
- **Template System**: Reusable document templates

## 🚀 Installation

### Standard Installation
```bash
pip install autobasedoc
```

### Development Installation
```bash
git clone https://github.com/NuCOS/autobasedoc.git
cd autobasedoc
pip install -e .
```

### Environment Setup Script
If you want to create a local virtual environment with all dependencies, you can
run the helper script:

```bash
./setup_env.sh
```

### Requirements
- Python 3.6+
- ReportLab 3.5+
- Matplotlib 3.0+
- Additional dependencies: svglib, pdfrw

## 📖 Quick Start

### Basic Document Creation

```python
import autobasedoc.autorpt as ar

# Create document with predefined templates
doc = ar.AutoDocTemplate(
    "my_report.pdf",
    onFirstPage=(ar.drawFirstPortrait, 0),
    onLaterPages=(ar.drawLaterPortrait, 0),
    title="My Professional Report"
)

# Initialize styles
styles = ar.Styles()

# Build content
content = []
content.append(ar.Paragraph("Executive Summary", styles.title))
content.append(ar.doTableOfContents())  # Auto-generated TOC
content.append(ar.Paragraph("Introduction", styles.h1))
content.append(ar.Paragraph("This is the content...", styles.normal))

# Generate PDF
doc.multiBuild(content)
```

### Multi-column Layout

```python
# Two-column landscape document
doc = ar.AutoDocTemplate(
    "newsletter.pdf",
    onFirstPage=(ar.drawFirstLandscape, 1),
    onLaterPages=(ar.drawLaterLandscape, 2),  # 2 columns
    pagesize=ar.landscape(ar.A4)
)
```

### Headers and Footers

```python
# Add professional headers and footers
doc.addPageInfo(typ="header", pos="l", text="Company Name")
doc.addPageInfo(typ="header", pos="r", text="Report Title")
doc.addPageInfo(typ="footer", pos="c", text="Page ", addPageNumber=True)
doc.addPageInfo(typ="footer", pos="r", text="Confidential")
```

### Matplotlib Integration

```python
import autobasedoc.autoplot as ap
import matplotlib.pyplot as plt

# Create a matplotlib figure
@ap.pdfplot()  # Decorator converts to PDF flowable
def create_chart():
    plt.figure(figsize=(8, 6))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3])
    plt.title("Sample Chart")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    return plt.gcf()

# Add to document
chart = create_chart()
content.append(chart)
```

## 📁 Project Structure

```
autobasedoc/
├── autobasedoc/
│   ├── __init__.py          # Package initialization
│   ├── autorpt.py           # Core document templates
│   ├── autoplot.py          # Matplotlib integration
│   ├── styles.py            # Styling system
│   ├── pageinfo.py          # Header/footer management
│   ├── fonts.py             # Font management
│   ├── styledtable.py       # Advanced table layouts
│   ├── tableofcontents.py   # TOC generation
│   └── fonts/               # Bundled fonts
├── tests/                   # Test suite and examples
├── sphinx_doc/                    # Documentation source
```

## 🎯 Use Cases

### Business Reports
- Financial statements with charts and tables
- Executive dashboards
- Performance reports with automated data visualization

### Technical Documentation
- API documentation with code examples
- Research papers with matplotlib plots
- User manuals with mixed layouts

### Academic Publications
- Thesis documents with automatic formatting
- Conference papers with figure management
- Lab reports with data visualization

## 🔧 Advanced Features

### Custom Page Templates
```python
def custom_page_template(canv, doc):
    """Custom page template with company branding"""
    # Add logo, watermarks, custom headers
    canv.drawImage("logo.png", 50, 750, width=100, height=50)
    # Custom frame configuration
    ar.addPlugin(canv, doc, frame="Custom")

doc = ar.AutoDocTemplate(
    "branded_report.pdf",
    onFirstPage=(custom_page_template, 0)
)
```

### Dynamic Content
```python
# Conditional page breaks
content.append(ar.PageBreak())

# Automatic figure numbering
content.append(ar.doImage(chart, doc, "Sales Chart", styles))

# Keep elements together
content.append(ar.KeepTogether([heading, table]))
```

### Table Styling
```python
from autobasedoc.styledtable import StyledTable

# Create styled table with automatic formatting
table = StyledTable([
    ["Product", "Q1", "Q2", "Q3", "Q4"],
    ["Widget A", "100", "120", "110", "130"],
    ["Widget B", "80", "90", "95", "105"]
])
table.setTableStyle("grid")  # Predefined styles
content.append(table)
```

## 📚 Documentation

- **Full Documentation**: http://autobasedoc.readthedocs.io/
- **API Reference**: Comprehensive function and class documentation
- **Examples Gallery**: Visual examples of different layouts
- **Tutorials**: Step-by-step guides for common tasks

## 🧪 Testing

### Run Test Suite
```bash
# Using pytest
pytest tests/

# Using nose2
nose2

# Run specific test file
python tests/test_autoreport.py
```

### Test Coverage
```bash
# Generate coverage report
pytest --cov=autobasedoc tests/
```

### Example Scripts
```bash
# Run basic example
python tests/example.py

# Run advanced document example
python tests/example_document.py
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

### Development Setup
```bash
git clone https://github.com/NuCOS/autobasedoc.git
cd autobasedoc
pip install -e ".[dev]"  # Install with development dependencies
```

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for new functions
- Include docstrings in NumPy format
- Write tests for new features

### Contribution Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Changelog

### Version 1.1.10 (Current)
- Enhanced matplotlib integration
- Improved table styling
- Bug fixes in frame management

### Version 1.1.x
- Multi-column layout support
- Advanced header/footer system
- Custom font management

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-party Licenses
- ReportLab: BSD License
- Matplotlib: PSF License
- See individual package documentation for complete license information

## 🆘 Support

### Getting Help
- **Documentation**: http://autobasedoc.readthedocs.io/
- **GitHub Issues**: Report bugs and request features
- **Stack Overflow**: Tag questions with `autobasedoc`

### Commercial Support
For commercial support and custom development, contact: contact@nucos.de

## 👥 Authors and Acknowledgments

- **Johannes Eckstein** - [@eckjoh2](https://twitter.com/eckjoh2) - Lead Developer
- **Oliver Braun** - Core Contributor

### Special Thanks
- ReportLab team for the excellent PDF library
- Matplotlib community for visualization tools
- Contributors and users providing feedback and improvements

## 🔗 Links

- **Homepage**: [https://github.com/NuCOS/autobasedoc](https://github.com/NuCOS/autobasedoc)
- **PyPI Package**: [https://pypi.org/project/autobasedoc/](https://pypi.org/project/autobasedoc/)
- **Documentation**: [http://autobasedoc.readthedocs.io/](http://autobasedoc.readthedocs.io/)
- **Issue Tracker**: [https://github.com/NuCOS/autobasedoc/issues](https://github.com/NuCOS/autobasedoc/issues)

---

*AutoBaseDoc - Making professional PDF generation simple and powerful.*
