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
                       QgsProcessingParameterField,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterString)
from pylusat import base, density

sys.path.append("..")

from pylusatq_utils import pylusatq_icon


class PointDensity(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    POINT = "POINT"
    POP_COLUMN = 'POP_COLUMN'
    SEARCH_RADIUS = "SEARCH_RADIUS"
    AREA_UNIT = "AREA_UNIT"
    OUTPUT_COLUMN = "OUTPUT_COLUMN"
    OUTPUT = "OUTPUT"

    def icon(self):
        return pylusatq_icon()

    def tr(self, string, context=''):
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)

    def group(self):
        return self.tr(self.groupId().capitalize())

    def groupId(self):
        return "density"

    def name(self):
        return "pointdensity"

    def displayName(self):
        return self.tr("Density of Point Features")

    def shortHelpString(self):
        html_doc = '''
        <p>Calculate density of point features within the specified \
        search radius of each input polygon features.</p>
        
        <h3>Input Layer</h3>
        <p>Input vector layer.</p>

        <h3>Point Layer</h3>
        <p>Input point layer.</p>

        <h3>Population Field</h3>
        <p>Field denoting population values for each point. The population \
        field is the count or quantity to be used in the calculation of a \
        continuous surface.</p>

        <h3>Search Radius</h3>
        <p>The search radius created around the polygons to calculate the \
        density. The default set is 0, which means the calculating area is \
        the area of each polygon feature. Units need to be specified.</p>

        <h3>Areal Unint</h3>
        <p>The desired area units of the output density values.</p>

        <h3>Output Column Name</h3>
        <p>Name of the column storing distances in the output layer.</p>

        <h3>Output</h3>
        <p>Output vector layer.</p>
        '''
        return html_doc

    def createInstance(self):
        return PointDensity()

    def __init__(self):
        super().__init__()
        self.area_unit = (
            ('Square meters', self.tr('Square meters')),
            ('Square kilometers', self.tr('Square kilometers')),
            ('Hectares', self.tr('Hectares')),
            ('Square feet', self.tr('Square feet')),
            ('Square miles', self.tr('Square miles')),
            ('Acres', self.tr('Acres'))
        )

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                types=[QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POINT,
                self.tr('Point layer'),
                types=[QgsProcessing.TypeVectorPoint]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.POP_COLUMN,
                self.tr('Population field'),
                parentLayerParameterName=self.POINT,
                type=QgsProcessingParameterField.Numeric,
                optional=True
            )
        )
        search_radius = QgsProcessingParameterDistance(
            self.SEARCH_RADIUS,
            self.tr('Search radius'),
            parentParameterName=self.INPUT
        )
        search_radius.setMetadata({
            'widget_wrapper': {
                'decimals': 2
            }
        })
        self.addParameter(search_radius)
        self.addParameter(
            QgsProcessingParameterEnum(
                self.AREA_UNIT,
                self.tr('Area unit (for density value)'),
                options=[u[1] for u in self.area_unit],
                defaultValue=0
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                name=self.OUTPUT_COLUMN,
                description=self.tr('Output column name'),
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_lyr = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        point_lyr = self.parameterAsVectorLayer(parameters, self.POINT, context)
        pop_clm = parameters[self.POP_COLUMN]
        search_radius = self.parameterAsDouble(parameters,
                                               self.SEARCH_RADIUS,
                                               context)
        area_unit = self.area_unit[self.parameterAsEnum(parameters,
                                                        self.AREA_UNIT,
                                                        context)][0]
        output_clm = self.parameterAsString(parameters,
                                            self.OUTPUT_COLUMN,
                                            context)
        output_shp = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))
        from pylusatq_utils import PyLUSATQUtils

        input_gdf = PyLUSATQUtils.vector_to_gdf(input_lyr)
        point_gdf = PyLUSATQUtils.vector_to_gdf(point_lyr)
        if search_radius:
            search_radius = (
                f'{search_radius} '
                f'{base.GeoDataFrameManager(input_gdf).geom_unit_name}'
            )
        input_gdf[output_clm] = density.of_point(input_gdf, point_gdf, pop_clm,
                                                 search_radius, area_unit)
        input_gdf.to_file(output_shp)
        return {self.OUTPUT: output_shp}
