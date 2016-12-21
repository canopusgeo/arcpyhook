# arcpyhook
Configure the current python conda or virtualenv environment sys.path to support importing arcpy. This module only works on Windows platform.
If ESRI ArcGIS installation is not found, an `ImportError` exception is thrown.

## Example usage:
```python
try:
    import arcpyhook
    import arcpy
except ImportError:
    # handel the error that arcpy cannot be found.
```

## Installation

You can pip install from GitHub:

    	pip install git+https://github.com/canopusgeo/arcpyhook.git --trusted-host github.com