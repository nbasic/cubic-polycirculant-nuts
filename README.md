# Cubic polycirculant nut graphs

This is a [SageMath](https://www.sagemath.org/) script which provides a computer assisted proof
of the nonexistance of cubic 4-circulant and cubic 5-circulant nut graphs. Moreover, it can also
display underlying graphs for which cubic k-circulant nut graphs may exist.

The software has to be provided with a list of underlying graphs. To generate such graph for
the case of cubic `k`-circulants, the [geng](https://pallini.di.uniroma1.it/) can be used:
`$ geng -c -D3 k underlying_k.g6`.

If you are using the software in your research, please cite this paper:

 * N. Bašić and I. Damnjanović, On cubic polycirculant nut graphs, _Comp. Appl. Math._ **44** (2025),
   265, [doi:10.1007/s40314-025-03218-7](https://doi.org/10.1007/s40314-025-03218-7).
