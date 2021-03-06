# -*- encoding: utf-8 -*-

__author__ = 'ray'
__date__ = '6/23/14'

"""
    tests.storage.test_entry
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Test for FeatureEntry

"""

import unittest
from georest.geo import Key, Feature
from georest.storage import Response, FeatureEntry, DummyFeatureStorage
from georest.storage import FeatureNotFound


class TestFeatureEntry(unittest.TestCase):
    def setUp(self):
        self.bucket = DummyFeatureStorage().create_bucket('test')

        self.test_key = Key.make_key(
            bucket=self.bucket.bucket_name, name='alice')

        self.test_feature1 = Feature.build_from_geometry(
            'POINT (8 8)', properties=dict(x=8, y=8),
        )
        self.test_feature2 = Feature.build_from_geometry(
            'POINT (8 8)', properties=dict(x=8, y=8, z=8),
        )

    def test_put_feature_without_revision(self):
        entry = FeatureEntry(self.bucket)
        response = entry.put_feature(self.test_key, self.test_feature1)

        self.assertIsInstance(response, Response)
        self.assertEqual(response.key, self.test_key)

    def test_put_feature_with_same_key_without_revision(self):
        entry = FeatureEntry(self.bucket)
        response = entry.put_feature(self.test_key, self.test_feature1)
        response = entry.put_feature(self.test_key, self.test_feature2)

        self.assertIsInstance(response, Response)
        self.assertEqual(response.key, self.test_key)

        response, feature = entry.get_feature(self.test_key)
        self.assertEqual(feature.key, self.test_key)
        self.assertTrue(feature.equals(self.test_feature2))

    def test_get_feature(self):
        test_key = Key.make_key(bucket=self.bucket.bucket_name, name='alice')
        test_feature1 = Feature.build_from_geometry(
            'POINT (8 8)', properties=dict(x=8, y=8),
        )

        entry = FeatureEntry(self.bucket)
        response = entry.put_feature(test_key, test_feature1)

        # get a feature
        response, feature = entry.get_feature(test_key)
        self.assertEqual(feature.key, test_key)
        self.assertTrue(feature.equals(test_feature1))

    def test_delete_feature(self):
        test_key = Key.make_key(bucket=self.bucket.bucket_name, name='alice')
        test_feature1 = Feature.build_from_geometry(
            'POINT (8 8)', properties=dict(x=8, y=8),
        )

        entry = FeatureEntry(self.bucket)
        response = entry.put_feature(test_key, test_feature1)

        # delete a feature
        response = entry.delete_feature(test_key)
        self.assertIsInstance(response, Response)
        self.assertEqual(response.key, test_key)
        self.assertRaises(FeatureNotFound, entry.get_feature, test_key)
