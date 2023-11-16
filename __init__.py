# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PyLUSATQ
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
__date__ = '2023-11-07'
__copyright__ = '(C) 2023 by Changjie chen'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PyLUSATQ class from file PyLUSATQ.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .pylusatq_plugin import PyLUSATQProviderPlugin
    return PyLUSATQProviderPlugin()
