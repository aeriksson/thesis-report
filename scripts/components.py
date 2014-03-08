from matplotlib import pyplot, rc
import math
import itertools
import random
from matplotlib.patches import Circle, ArrowStyle
from matplotlib.patches import FancyBboxPatch
from colorsys import hsv_to_rgb
import numpy

N_X = 36
N_Y = 18

SATURATION = 0.6
LIGHTNESS = 1.0

N_FIGURES = 8
FIGURE_WIDTH = 8
FIGURE_HEIGHT = FIGURE_WIDTH / 2.0
FIGURE_SIZE = (FIGURE_WIDTH, FIGURE_HEIGHT)

CIRCLE_RADIUS = 0.5

def mean_hue(hues):
    y = sum(math.sin(2 * math.pi * hue) for hue in hues)
    x = sum(math.cos(2 * math.pi * hue) for hue in hues)
    hue = math.atan2(y, x) / math.pi / 2.0
    if hue < 0:
        hue += 1.0
    return hue


def hue_dist(h1, h2):
    return min(abs(h1 - h2), abs(1 + h1 - h2), abs(1 + h2 - h1))


def hue_to_rgb(hue):
    return hsv_to_rgb(hue, SATURATION, LIGHTNESS)


def make_point(x, y, hue, x_index, y_index):
    return { 'x': x, 'y': y, 'hue': hue, 'x_i': x_index, 'y_i': y_index }


def create_initial_points(n_x, n_y):
    def get_hue(x, y):
        yoffs = 4.05
        u = (math.cos(x) + math.cos(y + yoffs)) / 2.0 + 1.0
        r = random.random() * 0.4
        cos_fac = math.cos(math.pow((x - 7.5) ** 2 + (y - 8.5) ** 2, .25))
       #  cos_fac *= 1 - (x / (N_X * 1.5))
        h = min(1, (cos_fac + u + 1) / 2.0)
        shift = 0.6
        return h + shift if h + shift <= 1 else h + shift - 1

    return [make_point(x, y, get_hue(x, y), x_i, y_i)
            for y_i, y in enumerate(range(n_y))
            for x_i, x in enumerate(range(n_x))]


def transform_initial_points(points):
    def pt(x, y, hue):
        return make_point(x * 3 + 1, y * 3 + 1, hue, x, y)

    def xy_to_index(x, y):
        return y * N_X + x

    def avg_hue(x, y):
        indices = [xy_to_index(xi, yi)
                   for xi in (x - 1, x, x + 1)
                   for yi in (y - 1, y, y + 1)
                   if 0 <= xi < N_X and 0 <= yi < N_Y]
        hues = [points[i]['hue'] for i in indices]
        return mean_hue(hues)

    return [pt(x, y, avg_hue(x * 3 + 1, y * 3 + 1)) for y in range(6) for x in range(12)]


def transform_output(points, scores):
    def pt(x, y, hue):
        return make_point(x * 3 + 1, y * 3 + 1, hue, x, y)

    def xy_to_index(x, y):
        return y * N_X + x

    new_pts = []
    scores_n_weights = [[] for _ in range(N_X * N_Y)]

    for pt, s in zip(points, scores):
        x = pt['x']
        y = pt['y']
        for (xp, yp) in itertools.product(range(max(x - 2, 0), min(x + 3, N_X)),
                                          range(max(y - 2, 0), min(y + 3, N_Y))):
            ds = abs(xp - x) + abs(yp - y)
            if ds == 4:
                wt = 1.0
            elif ds == 3:
                wt = 2.0
            elif ds == 2:
                wt = 4.0
            elif ds == 1:
                wt = 8.0
            else:
                wt = 1
            scores_n_weights[xy_to_index(xp, yp)].append((s, wt))

    new_pts = [{'x': x, 'y': y} for y in range(N_Y) for x in range(N_X)]

    new_scores = [sum(s * w for (s, w) in ss) / sum(w for (_, w) in ss) for ss in scores_n_weights]

    return new_pts, new_scores


def draw_points(plot, points, labels=None, circle_radius=CIRCLE_RADIUS):
    for p in points:
        plot.add_patch(Circle((p['x'], p['y']),
                              circle_radius,
                              fc=hue_to_rgb(p['hue']),
                              ec='w'))

    # if labels:
    #     for p, label in zip(points, labels):
    #         plot.annotate(label,
    #                     (p['x'] + FIGURE_WIDTH * 0.02, p['y'] - FIGURE_WIDTH * 0.2),
    #                     ha='left',
    #                     size=15)


def get_axis(figsize=FIGURE_SIZE, xlim=(-.5, N_X - .5), ylim=(-.5, N_Y - .5)):
    figure = pyplot.figure(figsize=figsize)
    plot = figure.gca()
    plot.set_xlim(*xlim)
    plot.set_ylim(*ylim)
    plot.set_xticks([])
    plot.set_xticks([])
    plot.set_yticks([])
    plot.set_axis_off()
    return plot


def draw_points_scores(points, scores, circle_radius=CIRCLE_RADIUS):
    plot = get_axis()

    for p, s in zip(points, ((1 - s) / 3.0 for s in scores)):
        plot.add_patch(Circle((p['x'], p['y']),
                              circle_radius,
                              fc=hue_to_rgb(s),
                              ec='w'))

    pyplot.tight_layout()
    pyplot.draw()

def plot_anomaly_score(points, scores):
    plot = get_axis(figsize=(FIGURE_WIDTH / 6.0, FIGURE_WIDTH / 6.0),
                    xlim=(5.5, 5.5 + N_X / 6.0),
                    ylim=(5.5, 5.5 + N_X / 6.0))

    for i, (p, s) in enumerate(zip(points, ((1 - s) / 3.0 for s in scores))):
        if i == 7:
            plot.add_patch(Circle((p['x'], p['y']),
                                6 * CIRCLE_RADIUS,
                                fc=hue_to_rgb(s),
                                ec='w'))

    pyplot.tight_layout()
    pyplot.draw()

def plot_input(points, circle_radius=CIRCLE_RADIUS):
    plot = get_axis()

    draw_points(plot, points, circle_radius=circle_radius)

    pyplot.tight_layout()
    pyplot.draw()


def plot_evaluation_set(points):
    plot = get_axis()

    delta = 0.2
    new_points = []
    for i, p in enumerate(points):
        if i % 2 == 0:
            newx = p['x'] + delta
        else:
            newx = p['x'] - delta
        if (i / (N_X / 3)) % 2 == 0:
            newy = p['y'] + delta
        else:
            newy = p['y'] - delta
        new_points.append(make_point(newx, newy, p['hue'], 0, 0))
    draw_points(plot, new_points, circle_radius=3 * CIRCLE_RADIUS - delta)

    dist = abs(points[1]['x'] - points[0]['x'])

    # for i, pt in enumerate(p for p in points if p['x_i'] % 2 == 0 and p['y_i'] % 2 == 0):
    #     padding = 1
    #     plot.add_patch(FancyBboxPatch((pt['x'] - padding, pt['y'] - padding),
    #                                   dist + 2 * padding,
    #                                   dist + 2 * padding,
    #                                   boxstyle="round,pad=0.4",
    #                                   fc=(0., 0., 0., 0.0),
    #                                   ec=(0., 0., 0.)))

    pyplot.tight_layout()
    pyplot.draw()


def plot_context(points):
    plot = get_axis(figsize=(FIGURE_WIDTH / 2.0, FIGURE_HEIGHT), xlim=(-.5, N_X / 2.0 - .5))

    context = [p for p in points if p['x'] <= 18 and not (6 < p['x'] < 11 and 6 < p['y'] < 11)]
    draw_points(plot, context, circle_radius=3 * CIRCLE_RADIUS)

    pyplot.tight_layout()
    pyplot.draw()


def plot_reference_set(points):
    plot = get_axis(figsize=(FIGURE_WIDTH / 2.0, FIGURE_HEIGHT), xlim=(-.5, N_X / 2.0 - .5))

    delta = 0.2
    new_points = []
    for i, p in enumerate(points):
        if i % 2 == 0:
            newx = p['x'] + delta
        else:
            newx = p['x'] - delta
        if (i / (N_X / 3)) % 2 == 0:
            newy = p['y'] + delta
        else:
            newy = p['y'] - delta
        new_points.append(make_point(newx, newy, p['hue'], 0, 0))

    context = [p for p in new_points if p['x'] <= 18 and not (6 < p['x'] < 11 and 6 < p['y'] < 11)]
    draw_points(plot, context, circle_radius=3 * CIRCLE_RADIUS - delta)

    dist = abs(points[1]['x'] - points[0]['x'])

    # for i, pt in enumerate(p for p in points if p['x_i'] % 2 == 0 and p['y_i'] % 2 == 0):
    #     if i != 7:
    #         padding = 1
    #         plot.add_patch(FancyBboxPatch((pt['x'] - padding, pt['y'] - padding),
    #                                     dist + 2 * padding,
    #                                     dist + 2 * padding,
    #                                     boxstyle="round,pad=0.4",
    #                                     fc=(0., 0., 0., 0.0),
    #                                     ec=(0., 0., 0.)))

    pyplot.tight_layout()
    pyplot.draw()


def plot_evaluation_item(points):
    plot = get_axis(figsize=(FIGURE_WIDTH / 6.0, FIGURE_WIDTH / 6.0),
                    xlim=(5.5, 5.5 + N_X / 6.0),
                    ylim=(5.5, 5.5 + N_X / 6.0))

    context = [p for p in points if 6 < p['x'] < 11 and 6 < p['y'] < 11]
    draw_points(plot, context, circle_radius=3 * CIRCLE_RADIUS)

    pyplot.tight_layout()
    pyplot.draw()


# def plot_reference_set(plot, points):
#     draw_points(plot, points, circle_radius=3 * CIRCLE_RADIUS)
#
#     dist = abs(points[1]['x'] - points[0]['x'])
#     padding = dist * 0.2
#
#     def xy_to_index(x, y):
#         return y * N_X / 3 + x
#
#     def add_box(x, y):
#         plot.add_patch(FancyBboxPatch((x - padding, y - padding),
#                                       dist + 2 * padding,
#                                       dist + 2 * padding,
#                                       boxstyle="round,pad=0.1",
#                                       fc=(1., .8, 1., 0.0),
#                                       ec=(0., 0., 0.),
#                                       linestyle='dashed'))
#
#     for p in (points[xy_to_index(x, y)] for x in (0, 2, 4) for y in (0, 2, 4) if not x == y == 2):
#         add_box(p['x'], p['y'])


def normalize(scores):
    return [(s - min(scores)) / (max(scores) - min(scores)) for s in scores]


def compute_centers(candidates):
    points = []

    for c in candidates:
        n = len(c)
        (x, y) = (sum(p['x'] for p in c) / float(n), sum(p['y'] for p in c) / float(n))
        pt = make_point(x, y, mean_hue(p['hue'] for p in c), 0, 0)
        points.append(pt)

    return points


def plot_scores(plot, points, scores):
    draw_points_scores(plot, points, scores)


def group_points(points):
    def xy_to_index(x, y):
        return y * N_X / 3 + x

    candidates = []

    for (i_y, y) in enumerate(range(N_Y / 3 / 2)):
        for (i_x, x) in enumerate(range(N_X / 3 / 2)):
            xx = x * 2
            yy = y * 2
            candidates.append([points[xy_to_index(xx, yy)],
                               points[xy_to_index(xx + 1, yy)],
                               points[xy_to_index(xx, yy + 1)],
                               points[xy_to_index(xx + 1, yy + 1)]])

    return candidates


def compute_scores(candidates):
    def xy_to_index(x, y):
        return y * N_X / 3 / 2 + x

#     def index_to_xy(i):
#         return (i % (N_X / 3 / 2), i / (N_X / 3 / 2))

    def anomaly_score(candidate, others):
        distances = sorted([sum(hue_dist(o[i]['hue'], candidate[i]['hue'])
            for i in range(4)) for o in others])
        return sum(distances) / float(len(distances))

    scores = []

    n_x = N_X / 6
    n_y = N_Y / 6

    for y in range(n_y):
        for x in range(n_x):
            indices = [xy_to_index(xi, yi)
                       for xi in (x - 1, x, x + 1)
                       for yi in (y - 1, y, y + 1)
                       if 0 <= xi < n_x and 0 <= yi < n_y and not (xi == x and yi == y)]

            reference_set = [candidates[i] for i in indices]

            scores.append(anomaly_score(candidates[xy_to_index(x, y)], reference_set))

    return scores

def compute_output(candidates, scores):
    results = []
    scores2 = []
    for candidate, score in zip(candidates, scores):
        for i in candidate:
            results.append(i)
            scores2.append(score)
    return results, scores2


# figures = [pyplot.figure(figsize=(FIGURE_SIZE)) for _ in range(N_FIGURES)]

initial_points = create_initial_points(N_X, N_Y)

reduced_points = transform_initial_points(initial_points)

candidates = group_points(reduced_points)

scores = compute_scores(candidates)
normalized_scores = normalize(scores)

(output, output_scores) = compute_output(candidates, normalized_scores)

plot_input(initial_points)
pyplot.savefig('../resources/components/input.eps', transparent=True, bbox_inches='tight', pad_inches=0)
plot_input(reduced_points, circle_radius=3 * CIRCLE_RADIUS)
pyplot.savefig('../resources/components/transformed_input.eps', transparent=True, bbox_inches='tight', pad_inches=0)
plot_evaluation_set(reduced_points)
pyplot.savefig('../resources/components/evaluation_set.eps', transparent=True, bbox_inches='tight', pad_inches=0)
plot_evaluation_item(reduced_points)
pyplot.savefig('../resources/components/evaluation_item.eps', transparent=True, bbox_inches='tight', pad_inches=0)
plot_context(reduced_points)
pyplot.savefig('../resources/components/context.eps', transparent=True, bbox_inches='tight', pad_inches=0)
plot_reference_set(reduced_points)
pyplot.savefig('../resources/components/reference_set.eps', transparent=True, bbox_inches='tight', pad_inches=0)
plot_anomaly_score(compute_centers(candidates), normalized_scores)
pyplot.savefig('../resources/components/anomaly_score.eps', transparent=True, bbox_inches='tight', pad_inches=0)
draw_points_scores(compute_centers(candidates), normalized_scores, circle_radius=6 * CIRCLE_RADIUS)
pyplot.savefig('../resources/components/anomaly_scores.eps', transparent=True, bbox_inches='tight', pad_inches=0)
draw_points_scores(output, output_scores, circle_radius=3 * CIRCLE_RADIUS)
pyplot.savefig('../resources/components/solution.eps', transparent=True, bbox_inches='tight', pad_inches=0)
draw_points_scores(*transform_output(output, output_scores))
pyplot.savefig('../resources/components/transformed_solution.eps', transparent=True, bbox_inches='tight', pad_inches=0)
