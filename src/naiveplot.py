#!/usr/bin/python
"""
NaivePlot - A very naive plotting library for the console
"""

COLORS = True

try:
    from colorama import init
    from termcolor import colored
    init()
except ImportError:
    COLORS = False


class Point(object):
    """Just a point

    You can create it and check the value
        >>> p1 = Point(1, 5)
        >>> print p1
        (1, 5)
        >>> p1.x == 1 and p1.y == 5
        True

    A point can be compared to another point
        >>> p2 = Point(1, 5)
        >>> p3 = Point(5, 1)
        >>> p1 == p2
        True
        >>> p1 == p3
        False
    """

    def __init__(self, x, y):
        """Provide two coordinates
        """
        self.x = x
        self.y = y
        self._done = False
        return

    def __iter__(self):
        """I am an iterator
        """
        self._done = False
        return self

    def next(self):
        """Get one element and no more
        """
        if self._done:
            raise StopIteration
        self._done = True
        return self

    def __cmp__(self, other):
        """Compare
        """
        return abs(self.x.__cmp__(other.x)) + abs(self.y.__cmp__(other.y))

    def __str__(self):
        """Get string
        """
        return str((self.x, self.y))


class ParaFunc(object):
    """Parametric Function.

    Let's make a circle and ensure that the angle pi gives us (-1,0):
        >>> from math import sin, cos, pi
        >>> pf = ParaFunc(cos, sin)
        >>> p1 = pf(pi)
        >>> eps = 1.0/1E6
        >>> (-1 - eps < p1.x < 1 + eps) and (-eps < p1.y < eps)
        True
    """

    def __init__(self, f, g):
        """Provide functions
        """
        self._f = f
        self._g = g
        return

    def __call__(self, t):
        """Get the value"""
        return Point(self._f(t), self._g(t))


class Rectangle(ParaFunc):
    """Rectangle, defined by the two diagonal corners.

    Let's make couple of rectangles and see if they overlap.
        >>> r11 = Rectangle(Point(1, 1), Point(4, 5))
        >>> r12 = Rectangle(Point(1.5, 3), Point(3.5, 4))
        >>> r21 = Rectangle(Point(2, 2), Point(3, 8))
        >>> r22 = Rectangle(Point(3, 8), Point(2, 2))
        >>> r31 = Rectangle(Point(0.1, 0.3), Point(0.7, 0.8))
        >>> r32 = Rectangle(Point(2.1, 9.3), Point(2.7, 9.8))
        >>> r41 = Rectangle(Point(-1.5, -1.5), Point(7.6, 7.6))
        >>> r11.overlap(r12)
        True
        >>> r11.overlap(r31)
        False
        >>> r11.overlap(r32)
        False
        >>> r21 == r22
        True
        >>> print r11
        ((1, 1), (4, 5))
        >>> plot = NaivePlot(42, 21, -2, 8, -2, 8)
        >>> plot.add_curve(Curve(r11, 0, 1, 0.002), 'a')
        >>> plot.add_curve(Curve(r12, 0, 1, 0.002), 'b')
        >>> plot.add_curve(Curve(r22, 0, 1, 0.002), 'c')
        >>> plot.add_curve(Curve(r41, 0, 1, 0.002), 'd')
        >>> print plot # doctest: +NORMALIZE_WHITESPACE
            NaivePlot, 42x21
                        ^       ccccc
                  dddddd|ddddddddddddddddddddddddddddddd
                  d     7       c   c                  d
                  d     |       c   c                  d
                  d     6       c   c                  d
                  d     |       c   c                  d
                  d     5   aaaacaaacaaaa              d
                  d     |   a   c   c   a              d
                  d     4   a bbcbbbcbb a              d
                  d     |   a b c   c b a              d
                  d     3   a bbcbbbcbb a              d
                  d     |   a   c   c   a              d
                  d     2   a   ccccc   a              d
                  d     |   a           a              d
                  d     1   aaaaaaaaaaaaa              d
                  d     |                              d
                2---1--d+---1---2---3---4---5---6---7---->
                  d     d                              d
                  d     1                              d
                  dddddd|ddddddddddddddddddddddddddddddd
                        2
        """

    def overlap(self, other):
        """Check if two rectangles have overlap.
        """
        if self._B.x < other._A.x or other._B.x < self._A.x:
            return False

        if self._B.y < other._A.y or other._B.y < self._A.y:
            return False

        return True

    def __init__(self, A, B):
        """Provide two points
        """
        ParaFunc.__init__(self, self._my_f, self._my_g)
        self._A = Point(min(A.x, B.x), min(A.y, B.y))
        self._B = Point(max(A.x, B.x), max(A.y, B.y))
        C = Point(self._B.x, self._A.y)
        D = Point(self._A.x, self._B.y)
        self._bottom = Line(self._A, C)
        self._right = Line(C, self._B)
        self._top = Line(self._B, D)
        self._left = Line(D, self._A)
        return

    def __cmp__(self, other):
        """Compare
        """
        return abs(self._A.__cmp__(other._A)) + abs(self._B.__cmp__(other._B))

    def __str__(self):
        """Get string
        """
        return "(%s, %s)" % (str(self._A), str(self._B))

    def _my_f(self, s):
        """X values.
        """
        if 0.00 <= s <= 0.25:
            return self._bottom._f(s*4)
        if 0.25 < s <= 0.50:
            return self._right._f(s*4-1)
        if 0.50 < s <= 0.75:
            return self._top._f(s*4-2)
        if 0.75 < s <= 1.00:
            return self._left._f(s*4-3)

    def _my_g(self, s):
        """Y values.
        """
        if 0.00 <= s <= 0.25:
            return self._bottom._g(s*4)
        if 0.25 < s <= 0.50:
            return self._right._g(s*4-1)
        if 0.50 < s <= 0.75:
            return self._top._g(s*4-2)
        if 0.75 < s <= 1.00:
            return self._left._g(s*4-3)


class Func(ParaFunc):
    """Regular function, a special case of ParaFunc

    Let's investigate a straight line:
        >>> f = Func(lambda x: 2+x)
        >>> Point(0, 2) == f(0)
        True
        >>> Point(1, 3) == f(1)
        True

    Let's investigate a polynomial:
        >>> f = Func(lambda x: (x+2)*(x-1)*(x-2))
        >>> eps = 1.0/1E6
        >>> [-eps < f(x).y < eps for x in [-2, 1, 2]]
        [True, True, True]
        >>> p1 = f(0)
        >>> p1.x == 0 and p1.y > 0
        True
    """

    def __init__(self, f):
        """Provide one function
        """
        ParaFunc.__init__(self, lambda t: t, f)
        return


class Line(ParaFunc):
    """A ParaFunc from Point A to Point B.
        >>> (a, b, c) = (Point(1, 1), Point(4, 1), Point (4, 4))
        >>> ab = Line(a, b)
        >>> bc = Line(b, c)
        >>> ca = Line(c, a)
        >>> print "The line ab is: '%s'" % ab
        The line ab is: 'Line from (1, 1) to (4, 1).'

        >>> plot = NaivePlot(12, 12, 1, 4, 1, 4)
        >>> for (l, nick) in [(ab, '-'), (bc, '|'), (ca, '/')]:
        ...     plot.add_curve(Curve(l, 0.0, 1.0, 0.01), nick)
        ...     plot.fit_curve(Curve(l, 0.0, 1.0, 0.01))
        >>> for (p, nick) in [(a, 'A'), (b, 'B'), (c, 'C')]:
        ...     plot.add_curve(p, 'o')
        >>> print plot
        NaivePlot, 12x12
                   o
                  /|
                 / |
                /  |
               /   |
              /    |
             /     |
            /      |
           /       |
          /        |
         /         |
        o----------o

    We can check if a point is on the line, with an optional precision.
        >>> ab.has_point(Point(2,1))
        True
        >>> ab.has_point(Point(2, 1.02), 0.1)
        True
        >>> ab.has_point(Point(2, 1.02), 0.01)
        False
    """

    def __init__(self, A, B):
        """Provide two points
        """
        self._A = A
        self._B = B

        if self._A.x != self._B.x:
            f = lambda t: self._A.x + t * (self._B.x - self._A.x)
        else:
            f = lambda t: self._A.x

        if self._A.y != self._B.y:
            g = lambda t: self._A.y + t * (self._B.y - self._A.y)
        else:
            g = lambda t: self._A.y

        ParaFunc.__init__(self, f, g)
        return

    def has_point(self, C, eps=0.0001):
        """Check if a point is on the line
        """
        # TODO: is s used or not?
        #s = (C.x - self._A.x) * (self._A.x - self._B.x) / self._B.x
        t = (C.y - self._A.y) * (self._A.y - self._B.y) / self._B.y
        return abs(C.y - self._g(t)) < eps

    def __str__(self):
        """String representation
        """
        return "Line from %s to %s." % (self._A, self._B)


class Histogram(Line):
    """Special case of Line, where one point is always on the x-axis,
    and the y-values are the same.

        >>> plot = NaivePlot(53, 13, 0, 13, 0, 10, refs = False)
        >>> sales = [ 1, 5, 6, 7, 2, 2, 12, 7, 2, 2, 7, 10]
        >>> for month in xrange(12):
        ...     hg = Histogram(Point(month+1, sales[month]))
        ...     c = Curve(hg, 0, 1, 0.01)
        ...     plot.add_curve(c, 's')
        ...     plot.fit_curve(c)
        >>> print plot # doctest: +NORMALIZE_WHITESPACE
        NaivePlot, 53x13
        ^                           s
        |                           s
        |                           s                   s
        |                           s                   s
        |                           s                   s
        |           s               s   s           s   s
        |           s   s           s   s           s   s
        |       s   s   s           s   s           s   s
        |       s   s   s           s   s           s   s
        |       s   s   s           s   s           s   s
        |       s   s   s   s   s   s   s   s   s   s   s
        |   s   s   s   s   s   s   s   s   s   s   s   s
        +--------------------------------------------------->
    """

    def __init__(self, A):
        """Provide a point A. Produce line from A to Point(A.x, 0)
        """
        B = Point(A.x, 0)
        Line.__init__(self, A, B)
        return


class Curve(object):
    """A curve is a function evaluated in certain points.
        >>> f = Func(lambda x: x+2)
        >>> c = Curve(f, 0, 9, 1)
        >>> points = [point for point in c]
        >>> points[0] == Point(0, f(0).y) == Point(0, 2)
        True
        >>> points[-1] == Point(9, f(9).y) == Point(9, 11)
        True
    """

    def __init__(self, parafunc, tmin, tmax, tgap):
        """Provide a ParaFunc (or Func), lower and upper limits and the gap
        """
        self._pf = parafunc
        self._tmin = tmin
        self._tmax = tmax
        self._tgap = tgap
        self._t = tmin - tgap
        return

    def __iter__(self):
        """I am an iterator
        """
        self._t = self._tmin - self._tgap
        return self

    def next(self):
        """Get the next point
        """
        self._t += self._tgap
        if self._t > self._tmax:
            raise StopIteration
        else:
            return self._pf(self._t)


class NaivePlot(object):
    """A plotter

    Two simple straignt lines
        >>> plt = NaivePlot(cols=7, rows=7, bg='.', refs=False)
        >>> c1 = Curve(ParaFunc(lambda t:   t, lambda t: 700), -750, 750, 10)
        >>> c2 = Curve(ParaFunc(lambda t: 700, lambda t:   t), -750, 750, 10)
        >>> plt.add_curve(c1, 'x')
        >>> plt.add_curve(c2, 'y')
        >>> plt.zoom(-700, 700, -700, 700)
        >>> print plt #doctest: +NORMALIZE_WHITESPACE
        NaivePlot, 7x7
        xxx^xxy
        ...|..y
        ...|..y
        ---+-->
        ...|..y
        ...|..y
        ...|..y
        >>>

    A fancy example with sinus:
        >>> from math import sin, pi
        >>> plot = NaivePlot(cols=31, rows=10)
        >>> c = Curve(Func(lambda x: sin(x)), -pi, pi, 0.01)
        >>> plot.add_curve(c, '.')
        >>> plot.fit_curve(c)
        >>> plot.set_size(62, 10)
        >>> plot.zoom(0, pi, -1, 1)
        >>> print plot # doctest: +NORMALIZE_WHITESPACE
        NaivePlot, 62x10
        ^
        |                ...........................
        |          .......                         .......
        |     ......                                     ......
        | .....                                               .....
        +d-----------------1------------------2-------------------3-->
        |
        |
        |
        1
        >>>
    """

    def __init__(self, cols=79, rows=23, xmin=-1.1, xmax=2.1, ymin=-1.1,
                 ymax=1.1, bg=' ', refs=True):
        """Default CTOR makes a panel
        """
        self._cols = cols
        self._rows = rows
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax
        self._plot = list()
        self._bg = bg
        self._curves = list()
        self._refs = refs
        return

    def zoom(self, xmin=None, xmax=None, ymin=None, ymax=None):
        """Reduce viewport
        """
        if xmin is not None:
            self._xmin = xmin
        if xmax is not None:
            self._xmax = xmax
        if ymin is not None:
            self._ymin = ymin
        if ymax is not None:
            self._ymax = ymax
        return

    def set_size(self, cols, rows):
        """Set number of columns and rows
        """
        self._cols = cols
        self._rows = rows
        return

    def add_curve(self, curve, cross, color=None):
        """Add a curve to the plot
        """
        self._curves.append((curve, cross, color))
        return

    def fit_curve(self, curve):
        """Adapt max/min for x/y of plot to match curve
        """
        for p in curve:
            self._xmin = min(self._xmin, p.x)
            self._xmax = max(self._xmax, p.x)
            self._ymin = min(self._ymin, p.y)
            self._ymax = max(self._ymax, p.y)
        return

    def add_axis(self):
        """Add axis
        """
        yaxis = ParaFunc(lambda t: 0, lambda t: t)
        self.add_curve(Curve(yaxis, self._ymin, self._ymax,
                             float(self._ymax - self._ymin)/self._rows/4), '|')
        self.add_curve(Point(0, self._ymin), '|')
        self.add_curve(Point(0, self._ymax), '|')

        xaxis = ParaFunc(lambda t: t, lambda t: 0)
        self.add_curve(Curve(xaxis, self._xmin, self._xmax,
                             float(self._xmax - self._xmin)/self._cols/4), '-')
        self.add_curve(Point(self._xmin, 0), '-')
        self.add_curve(Point(self._xmax, 0), '-')
        return

    def add_origo(self):
        """Just insert origo
        """
        self.add_curve(Point(0, 0), '+')
        return

    def add_axis_edges(self):
        """Add the points to the x and y axises.
        """
        self.add_curve(Point(0, self._ymax), '^')
        self.add_curve(Point(self._xmax, 0), '>')
        return

    def add_ref_values(self):
        """Insert coordinates like (0, 1), (0, 2), ...
        """
        pairs = list()

        for mini in ((0.001, 'm'), (0.01, 'c'), (0.1, 'd')):
            pairs.append((mini[0], mini[1]))
            pairs.append((-mini[0], mini[1]))

        for i in xrange(10):
            pairs.append((i, str(i)))
            pairs.append((-i, str(i)))

        for rom in ((10, 'X'), (50, 'L'), (100, 'C'), (500, 'D'), (1000, 'M')):
            pairs.append((rom[0], rom[1]))
            pairs.append((-rom[0], rom[1]))

        if self._xmin <= 0 <= self._xmax:
            for (value, nick) in pairs:
                if self._ymin <= value <= self._ymax:
                    self.add_curve(Point(0, value), nick)

        if self._ymin <= 0 <= self._ymax:
            for (value, nick) in pairs:
                if self._xmin <= value <= self._xmax:
                    self.add_curve(Point(value, 0), nick)
        return

    def get_coordinates(self, xval, yval):
        """Get index of row, col instead of float values
        """
        x = int((self._cols-1)*(xval - self._xmin) / (self._xmax - self._xmin))
        y = int((self._rows-1)*(yval - self._ymin) / (self._ymax - self._ymin))
        return (x, y)

    def __str__(self):
        """Make string representation
        """
        plot = list()
        for _ in xrange(self._rows):
            plot.append([self._bg] * self._cols)

        # TODO: these should be optional
        self.add_axis()
        if self._refs:
            self.add_ref_values()
        self.add_origo()
        self.add_axis_edges()

        output = "%s, %sx%s\n" % (self.__class__.__name__,
                                  self._cols, self._rows)

        for (curve, cross, color) in self._curves:
            for point in curve:
                if (self._xmin <= point.x <= self._xmax) and \
                        (self._ymin <= point.y <= self._ymax):
                    (x, y) = self.get_coordinates(point.x, point.y)
                    if COLORS and color is not None:
                        plot[y][x] = colored(cross, color)
                    else:
                        plot[y][x] = cross

        plot.reverse()
        for line in plot:
            output += "".join(line) + "\n"
        return output.rstrip()


if __name__ == '__main__':
    # doc tests below
    import doctest
    ret = doctest.testmod()
    print "%s tests of %s OK" % (ret.attempted-ret.failed, ret.attempted)
    print "Tests done."
