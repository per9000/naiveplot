#!/usr/bin/python

from argparse import ArgumentParser
from sys import stdin
from string import ascii_uppercase
from naiveplot import NaivePlot, Curve, Point, Line

class NaiveParserPlotter:
    """Class for reading and plotting"""

    def __init__(self):
        """Setup place holders"""
        self.args = None
        self.points = None
        self.lines = None
        self.colors = None
        self.plot = None
        return

    def setup(self):
        """Do all setup after parsing args"""
        self.get_handle()
        self.setup_formats()
        return


    def get_handle(self):
        """Get a handle to read from"""
        if self.args.std_in:
            self.handle = stdin
        elif self.args.in_file:
            self.handle = open(self.args.in_file, 'r')
        else:
            pass # TODO: exception?
        return

    def setup_formats(self):
        """Return format vectors"""
        self.points = list(ascii_uppercase)
        self.lines = ['.', '-', ':', '~', "'"]
        self.colors = ['blue', 'red', 'green', 'yellow', 'magenta', 'cyan',
                       'grey']  #'white'
        return

    def get_format(self, idx):
        """get approproate combo"""
        attrs = list()
        for container in [self.points, self.lines, self.colors]:
            attrs.append(container[idx%len(container)])
        return tuple(attrs)


    def parse_args(self, args=None):
        """Parse the arguments"""
        parser = ArgumentParser(description="Plot the numbers given in a file "
                                "or in stdin")

        rgroup = parser.add_argument_group("Read from...")
        rgroup.add_argument('--std-in', action="store_true", default=False,
                            help="Perform doc tests and exit instead.")
        rgroup.add_argument('--in-file', '-f', type=str, default=None,
                            help="Specify input file path.")

        dgroup = parser.add_argument_group("Input data...")
        dgroup.add_argument('--xy', '-x', action="store_true", default=False,
                            help="Treat first column as x values, and the "
                            "following as y-values (default False).")
        dgroup.add_argument('--col', '-c', action="append", dest='cols',
                            type=int, default=list(),
                            help="Specify which columns to investigate. "
                            "Repeat if needed. Default: All")
        dgroup.add_argument('--ignore-first', '-i', action="store_true",
                            default=False, help="ignore first line")
        dgroup.add_argument('--sep', '-s', default=' ',
                            help="Specify separator, default: space")

        fgroup = parser.add_argument_group("Formatting...")
        fgroup.add_argument('--gap', '-g', type=float, default=0.01,
                            help="inverted number of subpoints in lines")
        fgroup.add_argument('--not-implemented')

        if args:
            self.args = parser.parse_args(args)
        else:
            self.args = parser.parse_args()
        return


    def process(self):
        """Do the real work"""

        ctr = 0
        olds = None
        pcontainer = list()
        self.plot = NaivePlot(xmin=-0.1, ymin=-0.1)

        for line in self.handle:
            ctr += 1
            if ctr == 1 and self.args.ignore_first:
                continue

            values = [float(val.strip()) for val in \
                          line.strip().split(self.args.sep) if val]
            x = float(ctr)
            if self.args.xy:
                x = float(values[0])
            points = [Point(x, val) for val in values if x and val]
            pcontainer.append(points)

            if olds:
                for i in xrange(len(points)):

                    if not self.args.cols or i not in self.args.cols:
                        continue

                    if not olds[i] or not points[i]:
                        continue

                    l = Line(olds[i], points[i])
                    (_, lchar, lcol) = self.get_format(i)
                    self.plot.add_curve(Curve(l, 0.0, 1.0, self.args.gap),
                                        lchar, lcol)
            olds = points

        (xmin, xmax, ymin, ymax) = (0, 0, 0, 0)

        for points in pcontainer:
            for i in xrange(len(points)):

                if not self.args.cols or i not in self.args.cols:
                    continue

                (pchar, _,  pcol) = self.get_format(i)
                self.plot.add_curve(points[i], pchar, pcol)

                xmin = min(xmin, points[i].x)
                xmax = max(xmax, points[i].x)
                ymin = min(ymin, points[i].y)
                ymax = max(ymax, points[i].y)
        self.plot.zoom(xmin, xmax, ymin, ymax)
        return

    def __str__(self):
        """just print"""
        return str(self.plot)


if __name__ == "__main__":
    npp = NaiveParserPlotter()
    npp.parse_args()
    npp.setup()
    npp.process()
    print npp
