Introduction
------------
This programm implements seam carving, following
`Shai Adivan et al. 2007 <hhttps://perso.crans.org/frenoy/matlab2012/seamcarving.pdf>`_. This is done by calculating an
energy matrix by estimating the differences between the three colour channels in x- and y-direction. Then the path of
lowest energy in y-direction is searched by using dynamic programing.


