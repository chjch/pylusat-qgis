# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PyLUSATQ
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
__date__ = '2023-11-12'
__copyright__ = '(C) 2023 by Changjie chen'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import sys
import os
import inspect

from qgis.core import QgsApplication

from .pylusatq_provider import PyLUSATQProvider
sys.path.append(".algorithms")

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class PyLUSATQProviderPlugin:

    def __init__(self):
        self.provider = PyLUSATQProvider()

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'icons', 'icon.png')
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
