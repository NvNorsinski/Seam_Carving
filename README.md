# Introduction

This programm implements seam carving, following <a href="https://perso.crans.org/frenoy/matlab2012/seamcarving.pdf">
 Shai Adivan et al. 2007</a>
This is done by calculating an energy matrix by estimating the differences between the three colour channels in x- 
and y-direction. Then the path of lowest energy in y-direction is searched by using dynamic programing. Put images to
perform seam carving on in folder images/input. Results are stored in folder images/output.

## Author
* **Nils v. Norsinski**
---

> GitHub [@NvNorsinski](https://github.com/NvNorsinski)