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

from .qgis_processing.pylusatq import PyLUSATQProviderPlugin


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PyLUSATQG class from file PyLUSATQ.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    return PyLUSATQProviderPlugin()
