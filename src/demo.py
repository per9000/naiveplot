#!/usr/bin/python
"""
Demo for NaivePlot
"""

from math import sin, cos, pi
from naiveplot import Point, Line, Func, ParaFunc, Curve, NaivePlot


def heartx(t):
    return 16*(sin(t)**3)


def hearty(t):
    return 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t)


def curvex(s):
    return s


def curvey(s):
    return s - 8*cos(0.1*s) ** 3 + 0.003*s**2


if __name__ == '__main__':
    print "Demo Plot 1"
    plot = NaivePlot(xmin=-3.5, xmax=3.3, ymin=-3.3, ymax=2.7)
    c1 = Curve(Func(lambda x: 1-x/2), -pi, pi, 0.02)
    c2 = Curve(ParaFunc(lambda t: sin(2*t)-2,
                        lambda t: 2*cos(t)),
               0, 2*pi, 0.02)
    c3 = Curve(ParaFunc(lambda t: 2+sin(t),
                        lambda t: cos(t)-2),
               0, 2*pi, 0.02)

    for (curve, cross) in [(c1, '~'), (c2, '8'), (c3, 'o')]:
        plot.add_curve(curve, cross)
        plot.fit_curve(curve)

    for p in [1, -1, 2, -2]:
        plot.add_curve(Point(p, -p), 'X')
        plot.add_curve(Point(p,  p), 'X')
    print plot

    print "Demo Plot 2"
    heart = NaivePlot()
    pf1 = ParaFunc(heartx, hearty)
    c1 = Curve(pf1, -pi, pi, 0.001)
    heart.add_curve(c1, 'o')
    heart.fit_curve(c1)

    pf2 = ParaFunc(curvex, curvey)
    heart.add_curve(Curve(pf2, -20, 20, 0.01), 'x')

    print heart
    heart.zoom(-1, 17, -1, 17)
    print heart
    heart.zoom(10, 12, 10, 12)
    print heart

    f = open('swepop.csv', 'r')
    lines = f.read().split('\n')
    f.close()
    pplot = NaivePlot(xmin=1749, xmax=2013, cols=159)
    eplot = NaivePlot(xmin=1749, xmax=2013, cols=159)

    for line in lines[1:]:
        if not line.strip():
            # last line is blank
            continue
        (year, pop, births, deaths, _, __, mari, ___) = line.split(',')
        ppoint = Point(int(year), int(pop))
        pplot.add_curve(ppoint, '*')
        pplot.fit_curve(ppoint)

        if mari:
            mpoint = Point(int(year), int(mari))
            eplot.add_curve(mpoint, 'm')
            eplot.fit_curve(mpoint)

        bpoint = Point(int(year), int(births))
        dpoint = Point(int(year), int(deaths))
        eplot.add_curve(bpoint, '*')
        eplot.add_curve(dpoint, '-')
        eplot.fit_curve(bpoint)
        eplot.fit_curve(dpoint)

    for million in xrange(0, 10):
        pplot.add_curve(Point(pplot._xmin, million*1E6), str(million))
    for k in xrange(25000, 200000, 25000):
        eplot.add_curve(Point(eplot._xmin, k), '>')
        eplot.add_curve(Point(eplot._xmax, k), '<')
    print pplot
    print eplot

    print "Another Example - Pentagram"
    circ = ParaFunc(lambda t: 4+3*sin(t), lambda t: 4+3*cos(t))
    circle = Curve(circ, 0, 2*pi, 0.01)
    points = [circ(2*n*pi/5) for n in xrange(5)]
    lines = [Line(points[p], points[p+2]) for p in xrange(-2, 3)]
    pentagram = NaivePlot(36, 24, xmin=1, ymin=1)
    pentagram.add_curve(circle, '.')
    pentagram.fit_curve(circle)
    for line in lines:
        pentagram.add_curve(Curve(line, 0.0, 1.0, 0.01), '.')
    print pentagram
