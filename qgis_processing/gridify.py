import sys

from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterVectorDestination)
from pylusat.geotools import gridify
import geopandas as gpd

sys.path.append("..")

from .pylusatq_utils import pylusatq_icon


class Gridify(QgsProcessingAlgorithm):
    INPUT_GDF = "INPUT_GDF"  # defining variable for input gdf
    WIDTH = "WIDTH"  # defining variable for width
    HEIGHT = "HEIGHT"  # defining variable for height
    NUM_COLS = "NUM_COLS"  # defining variable for number of columns
    NUM_ROWS = "NUM_ROWS"  # defining variable for number of rows
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
            QgsProcessingParameterVectorLayer(
                self.INPUT_GDF,
                self.tr('Input GeoDataFrame')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.WIDTH,
                self.tr('Cell width')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.HEIGHT,
                self.tr('Cell height')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUM_COLS,
                self.tr('Number of columns')
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NUM_ROWS,
                self.tr('Number of rows')
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Output vector layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # processing
        in_gdf = gpd.read_file(
            self.parameterAsVectorLayer(
                parameters,
                self.INPUT_GDF,
                context
            ).dataProvider().dataSourceUri()
        )
        in_width = self.parameterAsInt(parameters,
                                       self.WIDTH,
                                       context)
        in_height = self.parameterAsInt(parameters,
                                        self.HEIGHT,
                                        context)
        in_cols = self.parameterAsInt(parameters,
                                      self.NUM_COLS,
                                      context)
        in_rows = self.parameterAsInt(parameters,
                                      self.NUM_ROWS,
                                      context)

        out_gdf = gridify(in_gdf, in_width, in_height, in_cols, in_rows)

        out_path = self.parameterAsOutputLayer(parameters,
                                               self.OUTPUT,
                                               context)
        
        out_layer = out_gdf.to_file(out_path)

        return {self.OUTPUT: out_layer}