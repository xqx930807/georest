# -*- encoding: utf-8 -*-

__author__ = 'kotaimen'
__date__ = '6/5/14'

import unittest

import shapely.geometry
import geojson
import json

from georest.geo.exceptions import InvalidGeometry, InvalidSpatialReference, \
    InvalidGeoJsonInput
from georest.geo.geometry import Geometry, \
    create_geometrycollection_from_geojson
from georest.geo.spatialref import SpatialReference

from tests.geo.data import jsondata, pydata


class TestGeometryCreation(unittest.TestCase):
    def test_wkt(self):
        geom1 = Geometry.make_geometry('POINT(1 2)')
        self.assertTrue(geom1.equals(shapely.geometry.Point(1, 2)))
        self.assertTrue(geom1._crs.equals(SpatialReference(srid=4326)))

        geom2 = Geometry.make_geometry('POINT(1 2)', srid=3857)
        self.assertTrue(geom2._crs.equals(SpatialReference(srid=3857)))

        geom3 = Geometry.make_geometry('SRID=3857;POINT(1 2)')
        self.assertTrue(geom3._crs.equals(SpatialReference(srid=3857)))

        geom4 = Geometry.make_geometry('SRID=3857;POINT(1 2)', srid=4326)
        self.assertTrue(geom4.equals(shapely.geometry.Point(1, 2)))
        self.assertTrue(geom4._crs.equals(SpatialReference(srid=3857)))

        geom5 = Geometry.make_geometry(
            'GEOMETRYCOLLECTION (POINT (2 2), LINESTRING (0 0, 1 1))')

        self.assertEqual(geom5.geom_type, 'GeometryCollection')

    def test_wkb(self):
        geom1 = Geometry.make_geometry(
            '0101000000000000000000F03F0000000000000040')
        self.assertTrue(geom1.equals(shapely.geometry.Point(1, 2)))
        self.assertTrue(geom1._crs.equals(SpatialReference(srid=4326)))

        geom2 = Geometry.make_geometry(
            b'\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\x00@')
        self.assertTrue(geom2.equals(shapely.geometry.Point(1, 2)))
        self.assertTrue(geom2._crs.equals(SpatialReference(srid=4326)))

    def test_geojson(self):
        geom1 = Geometry.make_geometry(
            '{ "type": "Point", "coordinates": [ 1.0, 2.0 ] }')
        self.assertTrue(geom1.equals(shapely.geometry.Point(1, 2)))
        self.assertTrue(geom1._crs.equals(SpatialReference(srid=4326)))

        geom2 = Geometry.make_geometry(
            u'{ "type": "Point", "coordinates": [ 1.0, 2.0 ] }')
        self.assertTrue(geom2.equals(shapely.geometry.Point(1, 2)))
        self.assertTrue(geom2._crs.equals(SpatialReference(srid=4326)))

    def test_failure(self):
        self.assertRaises(InvalidGeometry,
                          Geometry.make_geometry,
                          'bad')
        self.assertRaises(InvalidGeoJsonInput,
                          Geometry.make_geometry,
                          '{"type": "point", "coordinates": {bad} }')
        self.assertRaises(InvalidGeometry,
                          Geometry.make_geometry,
                          'POINT(1 2, x)')
        self.assertRaises(InvalidGeometry,
                          Geometry.make_geometry,
                          'POINT(1 2, 3, 4)')
        self.assertRaises(InvalidSpatialReference,
                          Geometry.make_geometry,
                          'POINT(1 2)',
                          srid=123456)
        self.assertRaises(InvalidGeometry,
                          Geometry.make_geometry,
                          'GEOMETRYCOLLECTION EMPTY')
        self.assertRaises(InvalidGeometry,
                          Geometry.make_geometry,
                          'POLYGON((0 0, 1 0, 0 1, 1 1, 0 0))', )

    def test_geometry(self):
        geom = shapely.geometry.Point(1, 2)
        geom2 = Geometry.make_geometry(geom)
        self.assertTrue(geom2._crs.equals(SpatialReference(srid=4326)))


class TestGeometryCollection(unittest.TestCase):
    def test_collection(self):
        geo_input = geojson.loads('''{
          "type": "GeometryCollection",
          "geometries": [
            {
              "type": "Point",
              "coordinates": [4.0,6.0]
            },
            {
              "type": "LineString",
              "coordinates": [[4.0,6.0],[7.0,10.0]]
            }
          ]
        }''')
        geometry = create_geometrycollection_from_geojson(geo_input)
        self.assertEqual(geometry.geom_type, 'GeometryCollection')

    def test_collection_empty(self):
        geo_input = geojson.loads('''{
          "type": "GeometryCollection",
          "geometries": []
        }''')
        geometry = create_geometrycollection_from_geojson(geo_input)
        self.assertEqual(geometry.geom_type, 'GeometryCollection')

    def test_collection_in_collection(self):
        geo_input = geojson.loads('''
        {
            "type": "GeometryCollection",
            "geometries": [
                {
                  "type": "Point",
                  "coordinates": [1.0, 1.0]
                },
                {
                  "type": "GeometryCollection",
                  "geometries": [
                    {
                      "type": "Point",
                      "coordinates": [4.0, 6.0]
                    },
                    {
                      "type": "LineString",
                      "coordinates": [[4.0, 6.0], [7.0, 10.0]]
                    }
                  ]
                }
            ]
        }
        ''')
        geometry = create_geometrycollection_from_geojson(geo_input)
        self.assertEqual(geometry.geom_type, 'GeometryCollection')


class TestGeometryTypes(unittest.TestCase):
    def test_geometry_types(self):
        for k, v in jsondata.iteritems():
            geometry = Geometry.make_geometry(v)
            self.assertDictEqual(
                json.loads(Geometry.export_geojson(geometry)),
                pydata[k]
            )


if __name__ == '__main__':
    unittest.main()
