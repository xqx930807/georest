# -*- encoding: utf-8 -*-

__author__ = 'pp'
__date__ = '6/18/14'


import mock
from georest.flaskapp import GeoRestApp


class ViewTestMixin(object):
    def setUp(self):
        with mock.patch('georest.storage.build_feature_storage') as mock_storage,\
                mock.patch('georest.model.FeaturesModel') as mock_feature_model,\
                mock.patch('georest.model.GeometryModel') as mock_geometry_model,\
                mock.patch('georest.model.FeaturePropertiesModel') as mock_feature_prop_model,\
                mock.patch('georest.model.OperationsModel') as mock_operations_model,\
                mock.patch('georest.model.AttributesModel') as mock_attributes_model:
            self.app = GeoRestApp(settings={'TESTING': True, 'STORAGE': {'prototype': 'dummy'}})

        self.mock_feature_model = mock_feature_model()
        self.mock_geometry_model = mock_geometry_model()
        self.mock_feature_prop_model = mock_feature_prop_model()
        self.mock_operations_model = mock_operations_model()
        self.mock_attributes_model = mock_attributes_model()

        self.client = self.app.test_client()

    def tearDown(self):
        pass
