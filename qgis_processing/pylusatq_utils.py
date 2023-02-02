# -*- coding: utf-8 -*-

"""
/***************************************************************************
 PyLUSATQGIS
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

# PyLUSATQ utilities library
import sys
import os

from collections import defaultdict
import pandas as pd
from shapely import wkt
import geopandas as gpd

sys.path.append("..")

from qgis.core import QgsVectorLayer
from qgis.PyQt.QtGui import QIcon


def pylusatq_icon():
    plugin_path = os.path.dirname(__file__)
    icon_folder = "icons"
    icon_file = "icon.png"
    return QIcon(os.path.join(plugin_path, icon_folder, icon_file))


class StringParameter:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self._validate()

    def _validate(self):
        if not isinstance(self.value, str):
            raise TypeError("'{}' must be a string.".format(self.name))

    def __repr__(self):
        return "{}('{}', '{}')".format(self.__class__.__name__,
                                       self.name, self.value)

    def __str__(self):
        return "'{}', '{}'".format(self.name, self.value)


class StringParameterNumber(StringParameter):

    def __init__(self, name, value):
        super().__init__(name, value)
        if not self._validate_number():
            raise ValueError("'{}' cannot be used as a "
                             "valid number.".format(self.value))

    def _validate_number(self):
        try:
            float(self.value)
            return True
        except ValueError:
            return False

    @property
    def as_number(self):
        if "." in self.value:
            return float(self.value)
        else:
            return int(self.value)


class StringParameterNumberList(StringParameter):

    def __init__(self, name, value):
        super().__init__(name, value)
        if not self._validate_number_list():
            raise ValueError(
                "f'{self.value}' is not a valid number list "
                "since {self.err}")

    def _validate_number_list(self):
        try:
            self.number_list = [
                StringParameterNumber("number", _.strip()).as_number
                for _ in self.value.split(",")
            ]
            return True
        except ValueError as err:
            self.err = err
            return False

    @property
    def as_number_list(self):
        return self.number_list


class StringParameterInterval(StringParameter):

    def __init__(self, name, value):
        super().__init__(name, value)
        self._validate_interval()

    def _validate_interval(self):
        if "-" not in self.value:
            raise ValueError("'{}' is not a valid interval. "
                             "Use '-' to separate the start and "
                             "the end of a interval.".format(self.value))
        else:
            _interval = self.value.split("-")
            if len(_interval) != 2:
                raise ValueError("'{}' is not a "
                                 "valid interval.".format(self.value))
            _start, _end = [StringParameterNumber('bound', _bound)
                            for _bound in _interval]
            if _start.as_number >= _end.as_number:
                raise ValueError("'{}' is not a valid interval. A interval's "
                                 "start value must be smaller than "
                                 "its end value.".format(self.value))
            else:
                self.start = _start.as_number
                self.end = _end.as_number

    @property
    def as_tuple(self):
        return self.start, self.end


class StringParameterIntervalList(StringParameter):

    def __init__(self, name, value, enforce_ascending=False):
        super().__init__(name, value)
        self.enforce_ascending = enforce_ascending
        if not self._validate_interval_list():
            raise ValueError("'{}' is not a valid definition, since '{}' "
                             "is not a valid list of intervals. "
                             "`if enforce_ascending == True`, make sure "
                             "bounds of each interval follows an ascending "
                             "order.".format(self.name, self.value))

    def _validate_interval_list(self):
        try:
            self.interval_list = [
                StringParameterInterval("interval", _.strip()).as_tuple
                for _ in self.value.split(",")
            ]
            if self.enforce_ascending:
                from itertools import chain
                chained_list = list(chain.from_iterable(self.interval_list))
                assert sorted(chained_list) == chained_list
            return True
        except AssertionError:
            return False

    @property
    def as_tuple_list(self):
        return self.interval_list


class StringParameterCategoryList(StringParameter):

    def __init__(self, name, value):
        super().__init__(name, value)
        if not self._validate_category_list():
            raise ValueError("{} is not a valid category list "
                             "since {}".format(self.value, self.err))

    def _validate_category_list(self):
        try:
            self.category_list = [StringParameter("category", _.strip()).value
                                  for _ in self.value.split(",")]
            return True
        except TypeError as err:
            self.err = err
            return False

    @property
    def as_category_list(self):
        return self.category_list


class PyLUSATQUtils:

    def __init__(self):
        self.agg_dict = defaultdict(set)

    def to_agg_dict(self, column: str, statistic: str):
        self.agg_dict[column].add(statistic)

    @staticmethod
    def _catch_null(attribute):
        try:
            if attribute.isNull():
                return None
        except AttributeError:
            return attribute

    @staticmethod
    def get_field_names(lyr: QgsVectorLayer) -> list:
        return [field.name() for field in lyr.fields()]

    @classmethod
    def attributes_to_df(cls, qgis_vector_lyr: QgsVectorLayer) -> pd.DataFrame:
        attributes_list = [
            [cls._catch_null(attr) for attr in feature.attributes()]
            for feature in qgis_vector_lyr.getFeatures()
        ]
        columns = cls.get_field_names(qgis_vector_lyr)
        return pd.DataFrame(attributes_list, columns=columns)

    @classmethod
    def vector_to_gdf(cls, qgis_vector_lyr: QgsVectorLayer) -> gpd.GeoDataFrame:
        feature_list = [
            [cls._catch_null(attr) for attr in feature.attributes()] +
            [feature.geometry().asWkt()]
            for feature in qgis_vector_lyr.getFeatures()
        ]

        columns = cls.get_field_names(qgis_vector_lyr)
        columns.append('geometry')
        df = pd.DataFrame(feature_list, columns=columns)

        df['geometry'] = df['geometry'].apply(wkt.loads)
        if qgis_vector_lyr.wkbType() == 6:   # if geometry is MultiPolygon
            df['geometry'] = df['geometry'].apply(
                lambda x: x[0] if len(x) == 1 else x
            )
        return gpd.GeoDataFrame(df, crs=qgis_vector_lyr.crs().toWkt(),
                                geometry='geometry')
