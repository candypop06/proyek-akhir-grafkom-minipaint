from collections import deque

def bresenham_line(x1, y1, x2, y2):

    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx - dy

    while True:

        points.append((x1, y1))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x1 += sx

        if e2 < dx:
            err += dx
            y1 += sy

    return points

def midpoint_circle(cx, cy, radius):

    points = []

    x = 0
    y = radius

    p = 1 - radius

    while x <= y:

        points.extend([
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y),

            (cx + y, cy + x),
            (cx - y, cy + x),
            (cx + y, cy - x),
            (cx - y, cy - x)
        ])

        x += 1

        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

    return points

def midpoint_ellipse(cx, cy, rx, ry):

    points = []

    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    while dx < dy:

        points.extend([
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y)
        ])

        x += 1
        dx = 2 * ry2 * x

        if p1 < 0:
            p1 += dx + ry2
        else:
            y -= 1
            dy = 2 * rx2 * y
            p1 += dx - dy + ry2

    p2 = (
        ry2 * (x + 0.5) ** 2 +
        rx2 * (y - 1) ** 2 -
        rx2 * ry2
    )

    while y >= 0:

        points.extend([
            (cx + x, cy + y),
            (cx - x, cy + y),
            (cx + x, cy - y),
            (cx - x, cy - y)
        ])

        y -= 1
        dy = 2 * rx2 * y

        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx = 2 * ry2 * x
            p2 += dx - dy + rx2

    return points

def flood_fill(canvas, x, y, fill_color):

    try:

        target = canvas.find_overlapping(x, y, x, y)

        if not target:
            return

        item = target[-1]

        canvas.itemconfig(
            item,
            fill=fill_color
        )

    except Exception:
        pass

def distance(x1, y1, x2, y2):

    return (
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    ) ** 0.5


def midpoint(p1, p2):

    return (
        (p1[0] + p2[0]) / 2,
        (p1[1] + p2[1]) / 2
    )