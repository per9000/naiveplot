naiveplot
=========

NaivePlot is a (yet another) library for making simple plotting in the terminal. Implemented in python it is perfect to visualize simple data, and pretty complex stuff too - but in an ascii-kinda-way.

    $ python
    Python 2.7.3 (default, Sep 26 2013, 20:08:41) 
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from math import sin, cos, pi
    >>> from naiveplot import Func, ParaFunc, Curve, NaivePlot
    >>> 
    >>> pf1 = ParaFunc(lambda t: 16*(sin(t)**3), 
    ...                lambda t: 13*cos(t) - 5*cos(2*t) - 2*cos(3*t) - cos(4*t))
    >>> c1 = Curve(pf1, -pi, pi, 0.001)
    >>> 
    >>> pf2 = Func(lambda s: s - 8*cos(0.1*s) ** 3 + 0.003*s**2)
    >>> c2 = Curve(pf2, -18, 18, 0.01)
    >>> 
    >>> heart = NaivePlot()
    >>> heart.add_curve(c1, 'o')
    >>> heart.add_curve(c2, 'x')
    >>> heart.fit_curve(c2)    
    >>> print heart
    NaivePlot, 79x23
                                           |                                      x
                                           |                                  xxxx 
                                           |                               xxxx    
                                           |                            xxxx       
                                           |                         xxxx          
                 oooooooooooooooooo        |       ooooooooooooooooxxx             
            oooooo                ooooo    X   ooooo            xxxxoooooo         
          ooo                         oooo 8oooo              xxx        ooo       
        ooo                              oo7o               xxx            ooo     
        o                                 o5               xx                o     
        o                                  4             xxx                 o     
        oo                                 2           xxx                  oo     
    -----------------X---8-7--6-5-4-3-2-1-d+-1-2-3-4-5--6-7-8---X----------------- 
           ooo                             2       xxx                  ooo        
             oooo                          3     xxx                 oooo          
                ooooo                      5   xxx               ooooo             
                    ooooo                  7xxxx             ooooo                 
                        ooooo            xx8x            ooooo                     
                            oxxxxxxxxxxxxx X         ooooo                         
                xxxxxxxxxxxxxx  ooooo      |     ooooo                             
            xxxxx                   oooo   |  oooo                                 
        xxxxx                          ooo |ooo                                    
    xxxxx                                oo|o                                      
    
    >>> 
