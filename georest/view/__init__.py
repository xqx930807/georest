# -*- encoding: utf-8 -*-

"""
    georest.view
    ~~~~~~~~~~~~~

    Restful resources
"""

__author__ = 'kotaimen'
__date__ = '3/19/14'

from flask import current_app
from flask.ext.restful import Resource

from .geometries import *
from .operations import *
from .features import *

from ..geo.jsonhelper import JSON_LIB_NAME

from ..geo.engine import describe
from .. import __version__


class Describe(Resource):
    def get(self):
        return {
            'version': __version__,
            'json_library': JSON_LIB_NAME,
            'geo_engine': describe(),
            'geo_store': current_app.store.describe(),
        }


del Resource
