# Cubic polycirculant nut graphs

This is a [SageMath](https://www.sagemath.org/) script which provides a computer assisted proof
of the nonexistance of cubic 4-circulant and cubic 5-circulant nut graphs. Moreover, it can also
display underlying graphs for which cubic k-circulant nut graphs may exist.

The software has to be provided with a list of underlying graphs. To generate such graph for
the case of cubic `k`-circulants, the [geng](https://pallini.di.uniroma1.it/) can be used:
`$ geng -c -D3 k underlying_k.g6`.
