# -*- encoding: utf-8 -*-

__author__ = 'kotaimen'
__date__ = '3/21/14'

import json

from flask import make_response, request
from flask.ext.restful import marshal_with, abort

from .base import BaseResource, make_header_from_feature, \
    make_response_from_geometry, GeometryRequestParser
from .fields import FEATURE_FIELDS

from ..geo.exception import GeoException

__all__ = ['Stat', 'GeometryResource', 'FeatureResource',
           'UnaryGeometryOperation']


class Stat(BaseResource):
    def get(self):
        return self.model.describe_capabilities()


class GeometryResource(BaseResource):
    parser = GeometryRequestParser()


    def get(self, key):
        args = self.parser.parse_args()
        feature = self.model.get_feature(key)
        headers = make_header_from_feature(feature)
        return make_response_from_geometry(feature.geometry,
                                           args.format,
                                           args.srid,
                                           headers)

    def post(self, key):
        data = request.data
        feature = self.model.put_feature(key, data)
        return None, 201, make_header_from_feature(feature)

    def delete(self, key):
        self.model.delete_feature(key)
        return None, 200


class FeatureResource(BaseResource):
    @marshal_with(FEATURE_FIELDS)
    def get(self, key):
        feature = self.model.get_feature(key)
        return feature, 200, make_header_from_feature(feature)





