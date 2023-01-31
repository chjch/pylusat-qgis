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
import os

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

# import processing algorithms
from .point_den import PointDensity
from .point_dist import PointDistance
from .line_dist import LineDistance
from .line_den import LineDensity
from .cell_dist import RasterCellDistance
from .idw import InverseDistanceWeighting
from .select_by_location import SelectByLocation
from .spatial_join import SpatialJoin
from .zonal_stats import ZonalStats
from .reclassify import Reclassify
from .linear_rescale import LinearRescale
from .ahp import AHP
from .weighted_sum import WeightedSum
from .identify_by_ranking import IdentifyByRanking
from .gridify import Gridify
from .raster_combine import RasterCombine

sys.path.append("..")

from .pylusatq_utils import pylusatq_icon


class PyLUSATQProvider(QgsProcessingProvider):

    def __init__(self):
        super().__init__()

    def algs_dict(self):
        return {PointDensity.__name__: PointDensity(),
                PointDistance.__name__: PointDistance(),
                LineDensity.__name__: LineDensity(),
                LineDistance.__name__: LineDistance(),
                RasterCellDistance.__name__: RasterCellDistance(),
                InverseDistanceWeighting.__name__: InverseDistanceWeighting(),
                SelectByLocation.__name__: SelectByLocation(),
                SpatialJoin.__name__: SpatialJoin(),
                ZonalStats.__name__: ZonalStats(),
                Reclassify.__name__: Reclassify(),
                LinearRescale.__name__: LinearRescale(),
                AHP.__name__: AHP(),
                WeightedSum.__name__: WeightedSum(),
                IdentifyByRanking.__name__: IdentifyByRanking(),
                Gridify.__name__: Gridify(),
                RasterCombine.__name__: RasterCombine()}

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
