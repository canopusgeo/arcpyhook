##    Copyright (C) 2016 Canopus GeoInformatics Ltd.
##
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License along
##    with this program; if not, If not, see <http://www.gnu.org/licenses/>.

'''
Configure the current python conda or virtualenv environment to support
importing arcpy. This module only works on Windows platform.
'''

from .arcpyhook import ArcpyInstallDir, Set_ArcpyPath

__all__ = [
    "__name__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
    "__summary__", "__url__",
]

__name__ = "arcpyhook"
__version__ = "0.1.0"
__author__ = "Canopus Geoinformatics, Ltd."
__email__ = "info@canopusgeo.com"
__license__ = "GPLv2"
__summary__ = __doc__
__copyright__ = "Copyright (C) 2016 Canopus GeoInformatics Ltd."
__url__ = "https://github.com/canopusgeo/arcpyhook"
