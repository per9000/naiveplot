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
        self.fvals = list()
        self.gvals = list()
        self.fboxes = list()
        self.gboxes = list()
        self.overlappers = None
        return

    def _seed(self, vals, container, func, funcvals):
        """Compute points on f or g for values of t or s
        """
        for idx in xrange(len(vals)-1):
            print "seed %s" % vals[idx]
            funcvals.append((vals[idx], func(vals[idx])))
            funcvals.append((vals[idx+1], func(vals[idx+1])))
            container.append(Rectangle(funcvals[-2][1], funcvals[-1][1]))
        return

    def seed_f(self, vals):
        """Compute points on f for values of t
        """
        self._seed(vals, self.fboxes, self.f, self.fvals)

    def seed_g(self, vals):
        """Compute points on g for values of s
        """
        self._seed(vals, self.gboxes, self.g, self.gvals)

    def get_delta_square(self, t, s):
        """Get the distance between two points, squared
        """
        p1 = self.f(t)
        p2 = self.g(s)
        return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

    def overlap(self):
        """Try to figure out if there is an overlap
        """
        self.overlappers = list()
        for fbox in self.fboxes:
            for gbox in self.gboxes:

                # TODO: remove illustration
                tmp = NaivePlot(60, 20, -1, 7, -1, 11)
                cf = Curve(self.f, 0.0, 1.0, 0.001)
                cg = Curve(self.g, 0.0, 1.0, 0.001)
                cfb = Curve(fbox, 0.0, 1.0, 0.001)
                cgb = Curve(gbox, 0.0, 1.0, 0.001)
                tmp.add_curve(cf, '/', 'white')
                tmp.add_curve(cg, '\\', 'white')
                tmp.add_curve(cfb, 'f', 'red')
                tmp.add_curve(cgb, 'g', 'blue')
                tmp.fit_curve(cf)
                tmp.fit_curve(cg)
                print tmp

                if fbox.overlap(gbox):
                    self.overlappers.append((fbox, gbox))
        return len(self.overlappers) > 0

    def seed(self, smin, smax, sstepsize, tmin, tmax, tstepsize):
        """True if the curves seems to have an intersection
        """
        self.seed_f(list(flt_range(smin, smax, sstepsize)))
        self.seed_g(list(flt_range(tmin, tmax, tstepsize)))
        return self.overlap()

    def _find_point(self, pnt, container, eps):
        """Find a value that was close to a point
        """
        print "Look for %s, in" % pnt,
        for items in container:
            print "{%s - %s}" % (items[0], items[1]),
        print eps
        eps = eps ** 2
        for (val, p) in container:
            print val,
            print p
            if pnt.distance_square(p) < eps:
                print "   found val %s" % val
                return val
        return

    def find_s(self, pnt, eps = 0.001):
        """Find the s value that corresponts to point pnt
        """
        return self._find_point(pnt, self.fvals, eps)

    def find_t(self, pnt, eps = 0.001):
        """Find the t value that corresponts to point pnt
        """
        return self._find_point(pnt, self.gvals, eps)

    def iterate(self):
        """Split all overlapping boxes in half and
        """
        new_overlappers = list()

        print "iterate"

        print self.f
        print self.g
        print self.fvals
        print self.gvals
        print self.fboxes
        print self.gboxes
        print self.overlappers

        for (fbox, gbox) in self.overlappers:
            print "fbox %s overlap with gbox %s" % (fbox, gbox)

            print "find s values using f"
            s1 = self.find_s(fbox.low())
            s3 = self.find_s(fbox.top())
            s2 = (s1+s3)/2
            self.seed_f([s2])
            f2 = self.fvals[-1]

            print "find t values using g"
            t1 = self.find_t(gbox.low())
            t3 = self.find_t(gbox.top())
            t2 = (t1+t3)/2
            self.seed_g([t2])
            g2 = self.gvals[-1]

            print "    (new s & t = %s & %s)" % (s2, t2)

            for fb in (Rectangle(fbox.low(), f2),
                       Rectangle(f2, fbox.high())):
                for gb in (Rectangle(gbox.low(), g2),
                           Rectangle(g2, gbox.high)):
                    if fb.overlap(gb):
                        print " new overlap of %s and %s " % (fb, gb)
                        new_overlappers.append((fb, gb))
        self.overlappers = new_overlappers
        return


if __name__ == '__main__':

    f = Line(Point(0, 0), Point(6, 10))
    g = Line(Point(1, 6), Point(3, 2))
    p = ParaSolver(f, g)

    print "Overlap? %s" % p.overlap()

    olap = p.seed(0.0, 1.0, 0.2, 0.0, 1.0, 0.2)
    print "Overlap? %s" % olap

    plot = NaivePlot(60, 20, -1, 7, -1, 11)
    plot.add_curve(Curve(f, 0.0, 1.0, 0.001), '/', 'white')
    plot.add_curve(Curve(g, 0.0, 1.0, 0.001), '\\', 'white')

    for _ in xrange(1):

        for (rbox, bbox) in p.overlappers:
            tmp_plot = NaivePlot(60, 20, -1, 7, -1, 11)
            tmp_plot.add_curve(Curve(f, 0.0, 1.0, 0.001), '/', 'white')
            tmp_plot.add_curve(Curve(g, 0.0, 1.0, 0.001), '\\', 'white')
            tmp_plot.add_curve(Curve(rbox, 0.0, 1.0, 0.001), 'f', 'red')
            tmp_plot.add_curve(Curve(bbox, 0.0, 1.0, 0.001), 'g', 'blue')
            print tmp_plot

            p.iterate()
