# PDF Tool

A command-line tool for PDF manipulation, built as a self-contained executable.

## Installation

```bash
./install.sh
```

## Usage

```bash
# Remove 36 points from all sides
pdf-tool document.pdf 36 36

# Remove different margins: left=20, top=30, right=25, bottom=35
pdf-tool document.pdf 20 30 25 35

# Works with absolute paths
pdf-tool /path/to/file.pdf 50 40
```

## Features

- ✅ Self-contained executable (no Python installation required)
- ✅ Fast startup (~0.1-0.3 seconds)
- ✅ Works from any directory
- ✅ Error handling and validation

## Examples

```bash
# Crop margins from a report
pdf-tool report.pdf 36 36

# Remove header/footer space
pdf-tool document.pdf 0 50 0 30

# Symmetric cropping
pdf-tool presentation.pdf 25 25
```

## Development

### Rebuilding:
```bash
./install.sh
```

### Manual build:
```bash
pyinstaller pdf-tool.spec
```
