"""
Where is the intersection between two parametric curves?
"""

from naiveplot import ParaFunc, NaivePlot, Curve


class ParaSolver(object):
    """The class that will find the intersection
    """

    def __init__(self, c1, c2):
        """Just a constructor
        """
        self.c1 = c1
        self.c2 = c2
        return

    def get_line(self, xmin, ymin, xmax, ymax):
        """Get tuple with (slope, yintercept)
        """
        slope = (ymax - ymin)/(xmax - xmin)
        intercept = (ymin+ymax)/2 - slope*(xmin+xmax)/2
        return (slope, intercept)

    def has_intersection(self, pair1, pair2):
        """True if the lines between points in pair1 and pair2 cross
        """
        #TODO: implement me
        print "%s %s" % (pair1, pair2)
        return

    def get_delta_square(self, t1, t2):
        """Get the distance between two points, squared
        """
        p1 = self.c1(t1)
        p2 = self.c2(t2)
        return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

    def iterate(self, tmin, tmax, smin, smax):
        """True if the curves seems to have an intersection
        """
        # TODO: store old values
        values = list()
        values.append(((tmin+tmax)/2, smin))
        values.append(((tmin+tmax)/2, smax))
        values.append(((tmin+tmax)/2, (smin+smax)/2))
        values.append((tmin, (smin+smax)/2))
        values.append((tmax, (smin+smax)/2))

        deltas = [self.get_delta_square(v[0], v[1]) for v in values]
        idx = deltas.index(min(deltas))

        # TODO: find the smallest delta with intersection
        _ = self.get_line(tmin, tmax, smin, smax)

        return values[idx]


if __name__ == '__main__':
    from math import pi
    from demo import heartx, hearty, curvex, curvey

    # the curves
    pf1 = ParaFunc(heartx, hearty)
    pf2 = ParaFunc(curvex, curvey)
    curve1 = Curve(pf1, -pi, pi, 0.01)
    curve2 = Curve(pf2, -20, 20, 0.01)

    # starting values for later
    points = list()
    (my_tmin, my_tmax) = (pi/4, pi/2)
    points.append(pf1(my_tmin))
    points.append(pf1(my_tmax))
    (my_smin, my_smax) = (9.22, 13.88)
    points.append(pf2(my_smin))
    points.append(pf2(my_smax))

    # get an overview of the problem
    plot = NaivePlot()
    plot.add_curve(curve1, 'o')
    plot.add_curve(curve2, 'x')

    # enter parasolver
    ps = ParaSolver(pf1, pf2)
    (s, t) = ps.iterate(my_tmin, my_tmax, my_smin, my_smax)
    ipoints = list()
    ipoints.append(pf1(s))
    ipoints.append(pf2(t))

    for point in points:
        plot.add_curve(point, 'A', 'white')
    for point in ipoints:
        plot.add_curve(point, 'B', 'red')

    (s, t) = ps.iterate(my_tmin, my_tmax, my_smin, my_smax)

    plot.zoom(-1, 17, -1, 17)

    print plot
