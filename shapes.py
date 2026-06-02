import math

def create_shape(
    shape_type,
    points,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    return {
        "type": shape_type,
        "points": points,

        "stroke_color": stroke_color,
        "fill_color": fill_color,

        "line_width": line_width,
        "line_style": line_style,

        "selected": False
    }

def create_point(
    x,
    y,
    stroke_color="black"
):

    return create_shape(
        "point",
        [(x, y)],
        stroke_color
    )

def create_line(
    p1,
    p2,
    stroke_color="black",
    line_width=2,
    line_style="solid"
):

    return create_shape(
        "line",
        [p1, p2],
        stroke_color,
        "",
        line_width,
        line_style
    )

def create_rectangle(
    p1,
    p2,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    x1, y1 = p1
    x2, y2 = p2

    points = [
        (x1, y1),
        (x2, y1),
        (x2, y2),
        (x1, y2)
    ]

    return create_shape(
        "rectangle",
        points,
        stroke_color,
        fill_color,
        line_width,
        line_style
    )

def create_triangle(
    p1,
    p2,
    p3,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    return create_shape(
        "triangle",
        [p1, p2, p3],
        stroke_color,
        fill_color,
        line_width,
        line_style
    )

def create_polygon(
    points,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    return create_shape(
        "polygon",
        points,
        stroke_color,
        fill_color,
        line_width,
        line_style
    )

def create_rhombus(
    p1,
    p2,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    x1, y1 = p1
    x2, y2 = p2

    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    points = [
        (cx, y1),
        (x2, cy),
        (cx, y2),
        (x1, cy)
    ]

    return create_shape(
        "rhombus",
        points,
        stroke_color,
        fill_color,
        line_width,
        line_style
    )

def create_parallelogram(
    p1,
    p2,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    x1, y1 = p1
    x2, y2 = p2

    offset = abs(x2 - x1) * 0.25

    points = [
        (x1 + offset, y1),
        (x2 + offset, y1),
        (x2, y2),
        (x1, y2)
    ]

    return create_shape(
        "parallelogram",
        points,
        stroke_color,
        fill_color,
        line_width,
        line_style
    )

def create_circle(
    center,
    radius,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    cx, cy = center

    return {
        "type": "circle",

        "center": (cx, cy),
        "radius": radius,

        "stroke_color": stroke_color,
        "fill_color": fill_color,

        "line_width": line_width,
        "line_style": line_style,

        "selected": False
    }

def create_ellipse(
    center,
    rx,
    ry,
    stroke_color="black",
    fill_color="",
    line_width=2,
    line_style="solid"
):

    cx, cy = center

    return {
        "type": "ellipse",

        "center": (cx, cy),

        "rx": rx,
        "ry": ry,

        "stroke_color": stroke_color,
        "fill_color": fill_color,

        "line_width": line_width,
        "line_style": line_style,

        "selected": False
    }

def get_bounding_box(shape):

    if shape["type"] == "circle":

        cx, cy = shape["center"]
        r = shape["radius"]

        return (
            cx - r,
            cy - r,
            cx + r,
            cy + r
        )

    if shape["type"] == "ellipse":

        cx, cy = shape["center"]

        rx = shape["rx"]
        ry = shape["ry"]

        return (
            cx - rx,
            cy - ry,
            cx + rx,
            cy + ry
        )

    pts = shape["points"]

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    return (
        min(xs),
        min(ys),
        max(xs),
        max(ys)
    )

def get_center(shape):

    if shape["type"] == "circle":
        return shape["center"]

    if shape["type"] == "ellipse":
        return shape["center"]

    x1, y1, x2, y2 = get_bounding_box(shape)

    return (
        (x1 + x2) / 2,
        (y1 + y2) / 2
    )

def contains_point(shape, x, y):

    x1, y1, x2, y2 = get_bounding_box(shape)

    return (
        x1 <= x <= x2 and
        y1 <= y <= y2
    )

def clone_shape(shape):

    import copy

    return copy.deepcopy(shape)