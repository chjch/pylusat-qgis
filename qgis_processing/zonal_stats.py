# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PyLUSATQGIS
 -----------
 The QGIS plugin for the PyLUSAT package.
 ------------
        begin                : 2021-10-02
        copyright            : (C) 2021 by Changjie chen
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
__date__ = '2021-10-02'
__copyright__ = '(C) 2021 by Changjie chen'

import sys
import os
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProcessingParameterVectorDestination)
from pylusat import zonal

sys.path.append("..")

from .pylusatq_utils import pylusatq_icon


class ZonalStats(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    RASTER = 'RASTER'
    STATS = 'STATS'
    OUTPUT_COLUMN_PREFIX = "OUTPUT_COLUMN_PREFIX"
    NODATA = 'NODATA'
    OUTPUT = 'ZonalStats'

    def icon(self):
        return pylusatq_icon()

    def tr(self, string, context=''):
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)

    def group(self):
        return self.tr(self.groupId().capitalize())

    def groupId(self):
        return 'overlay'

    def name(self):
        return 'zonalstats'

    def displayName(self):
        return self.tr('Zonal Statistics')

    def shortHelpString(self):
        html_doc = '''
        <p>Calculate statistics on values of raster within the zones of \
        another dataset.</p>

        <h3>Input layer</h3>
        <p>Dataset that defines the zones and sets boundaries according \
        to its geometries. The zones are only  defined by a vector layer.\
            </p>

        <h3>Raster layer</h3>
        <p>Raster that contains the values on which to calculate a \
        statistic.</p>

        <h3>Types of statistics</h3>
        <p>Statistic type to be calculate. 
 
        The types of statistics defaults to ['count', 'min', 'max', \
        'mean'].Other valid statistics are ['sum', 'std', 'median', \
        'majority','minority', 'unique', 'range'].

        Count—Count the number of cells have value, no data would not be \
        counted.

        Min(Minimum)—Determines the smallest value of all cells in the \
        value raster that belong to the same zone as the output cell.

        Max(Maximum)—Determines the largest value of all cells in the \
        value raster that belong to the same zone as the output cell.

        Mean—Calculates the average of all cells in the value raster that \
        belong to the same zone as the output cell.

        Sum—Calculates the total value of all cells in the value raster \
        that belong to the same zone as the output cell.

        Std(Standard deviation)—Calculates the standard deviation of all \
        cells in the value raster that belong to the same zone as the \
        output cell.

        Median—Determines the median value of all cells in the value \
        raster that belong to the same zone as the output cell.

        Majority—Determines the value that occurs most often of all \
        cells in the value raster that belong to the same zone as the \
        output cell.

        Minority—Determines the value that occurs least often of all \
        cells in the value raster that belong to the same zone as the \
        output cell.

        Unique—Count the number of unique value in cells.

        Range—Calculates the difference between the largest and smallest \
        value of all cells in the value raster that belong to the same \
        zone as the output cell.</p>

        <h3>No data value</h3>
        <p>Value should be considered as "no data" in the raster layer.\
        </p>

        <h3>Output layer</h3>
        <p>Output vector layer</p>
        '''
        return html_doc

    def createInstance(self):
        return ZonalStats()

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                types=[QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.RASTER,
                self.tr('Raster layer'),
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.STATS,
                self.tr('Types of statistics (separated by space)')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_COLUMN_PREFIX,
                self.tr('Output column prefix')
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NODATA,
                self.tr('No data value'),
                type=QgsProcessingParameterNumber.Integer,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Output layer'),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_lyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        raster_lyr = self.parameterAsRasterLayer(parameters, self.RASTER, context)
        stats = self.parameterAsString(parameters, self.STATS, context)
        output_clm_prefix = self.parameterAsString(parameters,
                                                   self.OUTPUT_COLUMN_PREFIX,
                                                   context)
        nodata = parameters[self.NODATA]
        output_file = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))
        from pylusatq_utils import PyLUSATQUtils

        input_gdf = PyLUSATQUtils.vector_to_gdf(input_lyr)
        raster_path = raster_lyr.dataProvider().dataSourceUri()

        output = zonal.zonal_stats_raster(input_gdf, raster_path, stats,
                                          output_clm_prefix, nodata)
        output.to_file(output_file, driver="GPKG")
        return {self.OUTPUT: output_file}
