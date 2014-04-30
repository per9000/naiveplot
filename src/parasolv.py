"""
Where is the intersection between two parametric curves?
"""

from naiveplot import ParaFunc, NaivePlot, Curve, Rectangle, Line, Point
from math import ceil
try:
    _xrange = xrange
except NameError:
    _xrange = range

def flt_range(start, stop=None, step=1.0):
    """
    Generates a set of floating point values over the range [start, stop)
    with step size step, inspired of http://code.activestate.com/recipes/66472
    """

    if stop is None:
        for x in _xrange(int(ceil(start/step))):
            yield x*step
    else:
        indices = (i for i in _xrange(0, int(ceil((stop-start)/step))))
        # yield results
        for i in indices:
            yield start + step*i
    return

class ParaSolver(object):
    """The class that will find the intersection
    """

    def __init__(self, f, g):
        """Just a constructor, given f(t) and g(s)
        """
        self.f = f
        self.g = g
        self.fboxes = list()
        self.gboxes = list()
        self.overlappers = None
        return

    def _seed(self, vals, container, func):
        """Compute points on f or g for values of t or s
        """
        for idx in xrange(len(vals)-1):
            container.append(Rectangle(func(vals[idx]), func(vals[idx+1])))
        return

    def seed_f(self, tvals):
        """Compute points on f for values of t
        """
        self._seed(tvals, self.fboxes, self.f)

    def seed_g(self, svals):
        """Compute points on g for values of s
        """
        self._seed(svals, self.gboxes, self.g)

    def get_delta_square(self, t, s):
        """Get the distance between two points, squared
        """
        p1 = self.f(t)
        p2 = self.g(s)
        return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

    def overlap(self):
        """Try to figure out if there is an overlap
        """
        for fbox in self.fboxes:
            for gbox in self.gboxes:
                if fbox.overlap(gbox):
                    self.overlappers = [fbox, gbox]
                    return True
        return False


    def iterate(self, tmin, tmax, tstepsize, smin, smax, sstepsize):
        """True if the curves seems to have an intersection
        """
        self.seed_f(list(flt_range(tmin, tmax, tstepsize)))
        self.seed_g(list(flt_range(smin, smax, sstepsize)))
        return self.overlap()


if __name__ == '__main__':

    f = Line(Point(0, 0), Point(6, 10))
    g = Line(Point(1, 6), Point(3, 2))
    p = ParaSolver(f, g)

    print "Overlap? %s" % p.overlap()

    p.iterate(0.0, 1.0, 0.2490, 0.0, 1.0, 0.2490)
    print "Overlap? %s" % p.overlap()

    plot = NaivePlot(60, 20, -1, 7, -1, 11)
    plot.add_curve(Curve(f, 0.0, 1.0, 0.001), '/', 'white')
    plot.add_curve(Curve(g, 0.0, 1.0, 0.001), '\\', 'white')
    plot.add_curve(Curve(p.overlappers[0], 0.0, 1.0, 0.001), 'f', 'red')
    plot.add_curve(Curve(p.overlappers[1], 0.0, 1.0, 0.001), 'g', 'blue')

    print plot

    plot.zoom(1, 4, 2, 6)

    print plot


