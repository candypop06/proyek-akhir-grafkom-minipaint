import math
import copy

def multiply_matrix(a, b):

    rows = len(a)
    cols = len(b[0])

    result = []

    for i in range(rows):

        row = []

        for j in range(cols):

            value = 0

            for k in range(len(b)):
                value += a[i][k] * b[k][j]

            row.append(value)

        result.append(row)

    return result

def point_to_matrix(point):

    x, y = point

    return [
        [x],
        [y],
        [1]
    ]

def transform_point(point, matrix):

    p = point_to_matrix(point)

    result = multiply_matrix(matrix, p)

    return (
        result[0][0],
        result[1][0]
    )

def transform_points(points, matrix):

    return [
        transform_point(p, matrix)
        for p in points
    ]

def translation_matrix(dx, dy):

    return [

        [1, 0, dx],

        [0, 1, dy],

        [0, 0, 1]
    ]

def rotation_matrix(angle):

    rad = math.radians(angle)

    c = math.cos(rad)
    s = math.sin(rad)

    return [

        [c, -s, 0],

        [s, c, 0],

        [0, 0, 1]
    ]

def scale_matrix(sx, sy):

    return [

        [sx, 0, 0],

        [0, sy, 0],

        [0, 0, 1]
    ]

def shear_x_matrix(shx):

    return [

        [1, shx, 0],

        [0, 1, 0],

        [0, 0, 1]
    ]

def shear_y_matrix(shy):

    return [

        [1, 0, 0],

        [shy, 1, 0],

        [0, 0, 1]
    ]

def get_points_center(points):

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    return (
        sum(xs) / len(xs),
        sum(ys) / len(ys)
    )

def rotate_points(points, angle):

    cx, cy = get_points_center(points)

    result = []

    rad = math.radians(angle)

    c = math.cos(rad)
    s = math.sin(rad)

    for x, y in points:

        tx = x - cx
        ty = y - cy

        rx = tx * c - ty * s
        ry = tx * s + ty * c

        result.append(
            (
                rx + cx,
                ry + cy
            )
        )

    return result

def scale_points(points, factor):

    cx, cy = get_points_center(points)

    result = []

    for x, y in points:

        nx = cx + (x - cx) * factor
        ny = cy + (y - cy) * factor

        result.append(
            (
                nx,
                ny
            )
        )

    return result

def shear_points_x(points, shx):

    cx, cy = get_points_center(points)

    result = []

    for x, y in points:

        tx = x - cx
        ty = y - cy

        nx = tx + shx * ty

        result.append(
            (
                nx + cx,
                ty + cy
            )
        )

    return result

def shear_points_y(points, shy):

    cx, cy = get_points_center(points)

    result = []

    for x, y in points:

        tx = x - cx
        ty = y - cy

        ny = ty + shy * tx

        result.append(
            (
                tx + cx,
                ny + cy
            )
        )

    return result

def translate_shape(shape, dx, dy):

    shape = copy.deepcopy(shape)

    if shape["type"] == "circle":

        cx, cy = shape["center"]

        shape["center"] = (
            cx + dx,
            cy + dy
        )

        return shape

    if shape["type"] == "ellipse":

        cx, cy = shape["center"]

        shape["center"] = (
            cx + dx,
            cy + dy
        )

        return shape

    matrix = translation_matrix(dx, dy)

    shape["points"] = transform_points(
        shape["points"],
        matrix
    )

    return shape

def rotate_shape(shape, angle):

    shape = copy.deepcopy(shape)

    if shape["type"] == "circle":

        return shape

    if shape["type"] == "ellipse":

        return shape

    shape["points"] = rotate_points(
        shape["points"],
        angle
    )

    return shape

def scale_shape(shape, factor):

    shape = copy.deepcopy(shape)

    if shape["type"] == "circle":

        shape["radius"] *= factor

        return shape

    if shape["type"] == "ellipse":

        shape["rx"] *= factor
        shape["ry"] *= factor

        return shape

    shape["points"] = scale_points(
        shape["points"],
        factor
    )

    return shape

def shear_shape_x(shape, shx):

    shape = copy.deepcopy(shape)

    if shape["type"] in ["circle", "ellipse"]:
        return shape

    shape["points"] = shear_points_x(
        shape["points"],
        shx
    )

    return shape

def shear_shape_y(shape, shy):

    shape = copy.deepcopy(shape)

    if shape["type"] in ["circle", "ellipse"]:
        return shape

    shape["points"] = shear_points_y(
        shape["points"],
        shy
    )

    return shape

def transform_shape(shape, matrix):

    shape = copy.deepcopy(shape)

    if "points" not in shape:
        return shape

    shape["points"] = transform_points(
        shape["points"],
        matrix
    )

    return shape

def bounding_box(points):

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    return (

        min(xs),

        min(ys),

        max(xs),

        max(ys)
    )

def shape_center(shape):

    if shape["type"] == "circle":
        return shape["center"]

    if shape["type"] == "ellipse":
        return shape["center"]

    return get_points_center(
        shape["points"]
    )

def animation_rotate(shape):

    return rotate_shape(
        shape,
        5
    )