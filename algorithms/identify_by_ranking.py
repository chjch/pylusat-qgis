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

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import sys

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing, QgsField, QgsFeature, QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterField,
                       QgsProcessingParameterFeatureSink)

sys.path.append("..")

from pylusatq_utils import pylusatq_icon


class IdentifyByRanking(QgsProcessingAlgorithm):

    INPUT = 'INPUT'
    INPUT_FIELD = 'INPUT_FIELD'
    FROM_TOP = 'FROM_TOP'
    NUMBER = 'NUMBER'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                types=[QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.INPUT_FIELD,
                self.tr('Base field'),
                parentLayerParameterName=self.INPUT
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FROM_TOP,
                self.tr('From top of the ranking'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUMBER,
                self.tr('Number of records'),
                type=QgsProcessingParameterNumber.Integer,
                defaultValue=5,
                optional=True
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Rank Identified')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        base_clm = self.parameterAsString(parameters, self.INPUT_FIELD,
                                          context)
        if_top = self.parameterAsBoolean(parameters, self.FROM_TOP, context)
        n = self.parameterAsInt(parameters, self.NUMBER, context)

        output_clm = f'TOP{n}' if if_top else f'LAST{n}'

        # get fields of input layer return a list of fields
        source_fields = source.fields()
        # append the new field to the existing fields
        source_fields.append(QgsField(output_clm, QVariant.Int))

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                                               context, source_fields,
                                               source.wkbType(),
                                               source.sourceCrs())

        # Compute the number of steps to display within the progress bar
        if source.featureCount():
            total = 100.0 / source.featureCount()
        else:
            total = 0

        features = sorted(source.getFeatures(),
                          key=lambda feat: feat[base_clm],
                          reverse=if_top)

        n_fid = [f.id() for f in features[:n]]

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            # create a feature with a list of fields
            f = QgsFeature()
            f_attrs = feature.attributes()
            f_attrs.append(1) if feature.id() in n_fid else f_attrs.append(0)
            f.setAttributes(f_attrs)

            # copy geometry from original feature
            f.setGeometry(feature.geometry())

            # Add a feature in the sink
            sink.addFeature(f, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))

        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Identify records by ranking'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId().capitalize())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'selection'

    def icon(self):
        return pylusatq_icon()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IdentifyByRanking()
