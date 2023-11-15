import sys

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorDestination)
from pylusat.geotools import gridify
import os

sys.path.append("..")

from pylusatq_utils import pylusatq_icon


class Gridify(QgsProcessingAlgorithm):
    INPUT = "INPUT"  # defining variable for input gdf
    CELL_X = "WIDTH"  # defining variable for width
    CELL_Y = "HEIGHT"  # defining variable for height
    N_COLS = "NUM_COLS"  # defining variable for number of columns
    N_ROWS = "NUM_ROWS"  # defining variable for number of rows
    OUTPUT = "OUTPUT"

    def icon(self):
        return pylusatq_icon()

    def tr(self, string, context=''):  # method to translate strings
        if context == '':
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)

    def group(self):
        return self.tr(self.groupId().capitalize())

    def groupId(self):
        return "overlay"

    def name(self):  # name of method
        return "Gridify"

    def displayName(self):  # name of method that will be displayed to the user
        return self.tr("Gridify")

    def shortHelpString(self):  # html document that explains what the tool is
        return self.tr("Creates grid based on the input_gdf.")

    def createInstance(self):
        return Gridify()

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                types=[QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CELL_X,
                self.tr('Cell size on the x-axis')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CELL_Y,
                self.tr('Cell size on the y-axis')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.N_COLS,
                self.tr('Number of columns')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.N_ROWS,
                self.tr('Number of rows')
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Output grid')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # processing
        input_lyr = self.parameterAsVectorLayer(parameters,
                                                 self.INPUT,
                                                 context)
        in_cell_x = self.parameterAsInt(parameters,
                                       self.CELL_X,
                                       context)
        in_cell_y = self.parameterAsInt(parameters,
                                        self.CELL_Y,
                                        context)
        in_cols = self.parameterAsInt(parameters,
                                      self.N_COLS,
                                      context)
        in_rows = self.parameterAsInt(parameters,
                                      self.N_ROWS,
                                      context)
        sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))
        from pylusatq_utils import PyLUSATQUtils
                
        input_gdf = PyLUSATQUtils.vector_to_gdf(input_lyr)

        out_gdf = gridify(input_gdf, in_cell_x, in_cell_y, in_cols, in_rows)

        out_path = self.parameterAsOutputLayer(parameters,
                                               self.OUTPUT,
                                               context)
        
        out_layer = out_gdf.to_file(out_path)

        return {self.OUTPUT: out_layer}