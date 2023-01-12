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
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterField,
                       QgsProcessingParameterString)
from pylusat import utils
from .pylusatq_utils import pylusatq_icon


class WeightedSum(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    FIELDS = "FIELDS"
    WEIGHTS = 'WEIGHTS'
    OUTPUT_COLUMN = "OUTPUT_COLUMN"
    OUTPUT = "WeightedSum"

    def icon(self):
        return pylusatq_icon()

    def tr(self, string, context=''):
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)

    def group(self):
        return self.tr(self.groupId().capitalize())

    def groupId(self):
        return "aggregation"

    def __init__(self):
        super().__init__()
        self.op_option = (
            ('Intersects', self.tr('Intersects')),
            ('Contains', self.tr('Contains')),
            ('Within', self.tr('Within'))
        )
        self.how_option = (
            ('Inner', self.tr('Inner')),
            ('Left', self.tr('Left')),
            ('Right', self.tr('Right'))
        )

    def name(self):
        return "weightedsum"

    def displayName(self):
        return self.tr("Weighted Sum of Fields")

    def shortHelpString(self):
        html_doc = '''
        <p>Calculate a weighted sum over a set of existing fields within the \
        input layer.</p>

        <h3>Input layer</h3>
        <p>Vecter layer being weighted</p>

        <h3>Fields</h3>
        <p>The field to use for weighting.

        The number of fields (second parameter) must equal to the number of weights \
        (third parameter).</p>

        <h3>Weights</h3>
        <p>Weight value by which to multiply the fields. It can be any positive \
        or negative decimal value. Weights should be separated by comma.</p>

        <h3>Output field</h3>
        <p>Output vector layer</p>
        '''
        return html_doc

    def createInstance(self):
        return WeightedSum()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                types=[QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELDS,
                self.tr('Fields'),
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
                allowMultiple=True
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.WEIGHTS,
                self.tr('Weights (equals to the number of fields)')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.OUTPUT_COLUMN,
                self.tr('Output field name')
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
        fields = self.parameterAsFields(parameters, self.FIELDS, context)
        weights = self.parameterAsString(parameters, self.WEIGHTS, context)
        output_clm = self.parameterAsString(parameters, self.OUTPUT_COLUMN, context)
        output_file = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))
        from pylusatq_utils import PyLUSATQUtils, StringParameterNumberList

        input_gdf = PyLUSATQUtils.vector_to_gdf(input_lyr)
        weights = StringParameterNumberList('weights', weights).as_number_list
        if len(fields) != len(weights):
            raise ValueError('Number of fields does not match the number of '
                             'weights provided.')
        fields_weights = dict(zip(fields, weights))

        input_gdf[output_clm] = utils.weighted_sum(input_gdf, fields_weights)
        input_gdf.to_file(output_file)
        return {self.OUTPUT: output_file}
