# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PyLUSATQGIS
 -----------
 The QGIS plugin for the PyLUSAT package.
 ------------
        begin                : 2022-11-02
        copyright            : (C) 2022 by Changjie chen
        email                : chj.chen@ufl.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Changjie chen'
__date__ = '2022-11-02'
__copyright__ = '(C) 2022 by Changjie chen'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import sys

from qgis.core import QgsProcessingProvider

sys.path.append("..")

# import processing algorithms
from .gridify import Gridify
from .pylusatq_utils import pylusatq_icon


class PyLUSATQProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()

    def algs_dict(self):
        return {Gridify.__name__: Gridify()}

    def loadAlgorithms(self):
        for alg in self.algs_dict().values():
            self.addAlgorithm(alg)

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'pylusatq'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('PyLUSAT Suitability Modeling')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return pylusatq_icon()

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.tr('PyLUSAT (Python for Land Use Suitability Analysis'
                       'Tools) QGIS plugin')

    def unload(self):
        pass
