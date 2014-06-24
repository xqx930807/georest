# -*- encoding: utf-8 -*-

"""
    georest.restapi
    ~~~~~~~~~~~~

    Rest API hub.
"""

import traceback

import flask

from . import geo
from . import view
from . import model


class GeoRestApi(object):
    """The API hub of georest"""

    def __init__(self, app):
        self.app = app
        self.add_resources()
        self.add_error_handler()

    def add_resource(self, resource, *urls, **kwargs):
        """utility method to add resources

        :param resource: flask view
        :param urls: url rules to apply
        :param kwargs: applied to app.add_url_rule as-is
        """
        for url_rule in urls:
            self.app.add_url_rule(url_rule, view_func=resource, **kwargs)

    def add_resources(self):
        """bind api urls to app"""
        feature_storage = self.app.feature_storage

        feature_model_config = self.app.config.get('FEATURE_MODEL', dict())
        feature_model = model.FeatureModel(feature_storage, **feature_model_config)
        geometry_model = model.GeometryModel(feature_storage, **feature_model_config)
        feature_prop_model = model.FeaturePropertiesModel(feature_storage, **feature_model_config)

        self.add_resource(view.describe, '/describe',
                          endpoint='describe')
        self.add_resource(view.Features.as_view('features', feature_model),
                          '/features',
                          '/features/<key>',
                          endpoint='features')
        self.add_resource(view.Geometry.as_view('geometry', geometry_model),
                          '/features/<key>/geometry',
                          '/geometries/<key>',
                          '/geometries',
                          '/features/geometry',
                          endpoint='geometry')
        self.add_resource(view.Properties.as_view('properties',
                                                  feature_prop_model),
                          '/features/<key>/properties',
                          endpoint='properties')

    def add_error_handler(self):
        self.app.errorhandler(geo.GeoException)(rest_error)


def rest_error(e):
    code = getattr(e, 'HTTP_STATUS_CODE', 500)
    response = flask.jsonify(dict(code=code,
                                  message=str(e),
                                  exception=e.__class__.__name__,
                                  traceback=traceback.format_tb(e.traceback)))
    response.status_code = code
    return response
