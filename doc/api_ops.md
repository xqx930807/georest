# Geometry operation API

## Operations

### Unary

Unary Geometry Properties

Operation | Parameters | result    | Description
--------- | ---------- | --------- | -----------
area      | `srid`     | pod/float | Area of the geometry in `srid` unit

Unary Topological Properties

Operation | Parameters | result    | Description
--------- | ---------- | --------- | -----------
boundary  | `srid`     | geojson   | Boundary of the geometry

Unary Topological Methods

Operation | Parameters                  | result    | Description
--------- | --------------------------- | --------- | -----------
buffer    | `width`, `quadsegs`, `srid` | geojson   | Returns a geometry that represents all points whose distance from this geometry is less than or equal to the given width.


### Binary

Binary Geometry Predicates

Operation | result    | Description
--------- | --------- | -----------
overlaps  | pod/bool  | Returns True if the DE-9IM intersection matrix for the two geometries is `T*T***T**` (for two points or two surfaces) `1*T***T**` (for two curves).

Binary Geometry Methods

Operation | result     | Description
--------- | ---------- | -----------
distance  | pod/float  | Returns the distance between the closest points on this geometry and the other geometry

Binary Topological Methods

Operation    | Parameters | result    | Description
------------ | ---------- | --------- | -----------
intersection | `srid`     | geojson   | Returns a geometry representing the points shared by this geometry and other.


### Variadic

Operation | Parameters | result    | Description
--------- | ---------- | --------- | -----------
union     | `srid`     | geojson   | Returns a geometry representing all the points in all given geometries.

## Query parameters

## Request

### URL pattern

```
/ops/:op/:key  # for unary operations
/ops/:op/:key1/:key2  # for binary operations
/ops/:op/:keys-split-by-slash  # for variadic operations
```

### GET method

When using `GET` method, all geometry-keys **MUST** exist.

For example:

```
GET /ops/overlaps/foo.bar/hodor.hodor
```

### POST method

When using `POST` method:

  - the posted content **MUST** be geojson geometry.
  - `~` can be used as a key, to represent the posted geometry.
  - `~.<i>` can also be used as a key, When posted geometry is a 
    multi-geometry(e.g. geometry collection), to represent the `<i>`th
    sub-geometry in the posted geometry, start from **0**.

For example:

```
POST /ops/overlaps/~/hodor.hodor

-d
{
  "type": "Point",
  "coordinates": [100, 105]
}
```

```
POST /ops/overlaps/~.0/~.1

-d
{
  "type": "GeometryCollection",
  "geometries": [
    {
      "type": "Point",
      "coordinates": [100, 105]
    },
    {
      "type": "Polygon",
      "coordinates": [
        [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
      ]
    }
  ]
}
```

## Response

When result type is geojson, a success operation response is **ALWAYS** geojson
document, representing the resulted geometry.

For example, response of `GET /ops/boundary/ranch.sheep`:

```json
{
  "type": "MultiLineString",
  "coordinates": [[
    [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
  ]]
}
```

When result type is pod, a success operation returns a json object with
"result" key that bears the pod result.

For example, response of `GET /ops/area/ranch.sheep`:

```json
{
  "result": 42.0
}
```

## Attributes

Simple way to access geometry attributes is provided.

### Request

```
GET /features/:key/geometry/attributes  # get interesting attributes of the geometry
GET /features/:key/geometry/attributes/:op_name  # same as /operations/:op_name/:key
```

query arguments are provided for the first variation, to include extra attributes,
or exclude some unnecessary attributes.

e.g.
```
GET /features/:key/geometry/attributes?include_length=t&exclude_area=1
```

this request will always include `length` attribute
and exclude `area` attribute.

### Response

the result will be a json object, with attribute names as keys and attribute
result as values.
