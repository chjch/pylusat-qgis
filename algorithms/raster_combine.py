from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination,
    QgsProcessingOutputString,
)
from pylusat.base import RasterManager
from pylusat.geotools import combine
from rasterio.shutil import copy
from ..pylusatq_utils import pylusatq_icon


class RasterCombine(QgsProcessingAlgorithm):
    INPUT = "INPUT"  # defining variable for first input
    INPUT2 = "INPUT2"  # defining variable for second input
    OUTPUT = "OUTPUT"  # defining variable for output
    ATT = "ATT"  # output attribute table for combined rasters

    def icon(self):
        return pylusatq_icon()

    def tr(self, string, context=""):  # method to translate strings
        if context == "":
            context = self.__class__.__name__
        return QCoreApplication.translate(context, string)

    def group(self):
        return self.tr(self.groupId().capitalize())

    def groupId(self):
        return "overlay"

    def name(self):  # name of method
        return "RasterCombine"

    def displayName(self):  # name of method that will be displayed to the user
        return self.tr("Raster Combine")

    def shortHelpString(self):  # html document that explains what the tool is
        return self.tr(
            "Combines multiple rasters by their unique combinations."
        )

    def createInstance(self):
        return RasterCombine()

    def __init__(self):
        super().__init__()

    def initAlgorithm(self, config=None):
        self.addParameter(  # adding first parameter to the qgis gui
            QgsProcessingParameterRasterLayer(  # raster layer is INPUT
                self.INPUT, self.tr("Input raster file path")
            )
        )
        # adding second parameter to the qgis gui
        self.addParameter(
            QgsProcessingParameterRasterLayer(  # raster layer is INPUT2
                self.INPUT2, self.tr("Input raster file path")
            )
        )
        # adding parameter for output file path to qgis gui
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT, self.tr("File path for output raster")
            )
        )

        self.addOutput(
            QgsProcessingOutputString(
                self.ATT, self.tr("Attribute table for output raster")
            )
        )

    def processAlgorithm(self, parameters, context, feedback):  # processing
        in_ras1 = self.parameterAsRasterLayer(parameters, self.INPUT, context)
        in_ras1_path = in_ras1.dataProvider().dataSourceUri()
        in_ras2 = self.parameterAsRasterLayer(parameters, self.INPUT2, context)
        in_ras2_path = in_ras2.dataProvider().dataSourceUri()

        ras_obj1 = RasterManager.from_path(in_ras1_path)
        ras_obj2 = RasterManager.from_path(in_ras2_path)

        new_obj1 = ras_obj1.match_extent(ras_obj2)
        new_obj2 = ras_obj2.match_extent(ras_obj1)

        combined_obj = combine(new_obj1, new_obj2)

        out_ras = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)
        copy(combined_obj[0], out_ras)

        return {self.OUTPUT: out_ras, self.ATT: combined_obj[1]}
