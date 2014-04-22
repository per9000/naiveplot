"""
Where is the intersection between two parametric curves?
"""

from naiveplot import NaivePlot


class Curve:
    """A curve has two equations, a starting and an end point.
    """

    def __init__(self, funcx, funcy):
        """Give me two functions and start/stop values
        """
        self.funcx = funcx
        self.funcy = funcy
        return

    def get_value(self, t):
        """Get the point for a given t
        """
        return (self.funcx(t), self.funcy(t))

    def cuts_origo(self, tmin, tmax):
        """True if the curve seems to cut origo diagonally.
        """
        (xmin, ymin) = (self.funcx(tmin), self.funcy(tmin))
        (xmax, ymax) = (self.funcx(tmax), self.funcy(tmax))

        # both x and y have to change sign
        if not (xmin < 0 < xmax or xmax < 0 < xmin):
            return False

        if not (ymin < 0 < ymax or ymax < 0 < ymin):
            return False

    def get_values(self, tmin, tmax, tgap):
        """Get values for the curve from tmin to tmax with a step size of tgap.
        """
        t = tmin
        output = list()
        while t < tmax:
            t += tgap
            output.append(self.get_value(t))
        return output


class ParaSolver:
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

    def get_delta_square(self, t1, t2):
        """Get the distance between two points
        """
        (x1, y1) = self.c1.get_value(t1)
        (x2, y2) = self.c2.get_value(t2)
        return (x1-x2)**2 + (y1-y2)**2

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
        return values[idx]


def heartx(t):
    return 16*(sin(t)**3)


def hearty(t):
    return 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t)


def curvex(s):
    return s


def curvey(s):
    return s - 8*cos(0.1*s) ** 3 + 0.003*s**2


if __name__ == '__main__':
    from math import sin, cos, pi

    # the curves
    c1 = Curve(heartx, hearty)
    c2 = Curve(curvex, curvey)

    # starting values for later
    points = list()
    (tmin, tmax) = (18*pi/60,  26*pi/60)
    (smin, smax) = (9.22, 13.88)
    points.append(c1.get_value(tmin))
    points.append(c1.get_value(tmax))
    points.append(c2.get_value(smin))
    points.append(c2.get_value(smax))

    # get an overview of the problem
    plot = NaivePlot()
    plot.plotparafunc(c1.funcx, c1.funcy, -pi, pi, 0.01, 'o')
    plot.plotparafunc(c2.funcx, c2.funcy, -20, 20, 0.01, 'x')

    # enter parasolber
    ps = ParaSolver(c1, c2)
    (s, t) = ps.iterate(tmin, tmax, smin, smax)
    ipoints = list()
    ipoints.append(c1.get_value(s))
    ipoints.append(c2.get_value(t))

    plot.plotvalues([p[0] for p in points], [p[1] for p in points], 'P')
    plot.plotvalues([p[0] for p in ipoints], [p[1] for p in ipoints], 'R')

    plot.zoom(-1, 17, -1, 17)

    print plot
