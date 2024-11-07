#!/usr/bin/env sage
from sage.all import *

from underlying_graphs import simple

def is_matching(edges):
    '''
    Return True if the list of edges contains a matching (not necessarily a perfect matching).
    '''
    vert = set()
    for u, v in edges:
        if u in vert:
            return False
        vert.add(u)
        if v in vert:
            return False
        vert.add(v)
    return True

def contains_isomorphic(l, h):
    '''
    Returns True if the list l contains a graph that is isomorphic to h.
    '''
    for g in l:
        if g.is_isomorphic(h):
            return True
    return False

def make_all_covers(g):
    '''
    Takes a graphs g, and returns a list of all cubic pregraphs obtained from underlying graph g.
    Underlying graph of a pregraph h is a simple graph, which is obtained from h by removing all
    loops, semi edges and duplicate edges.
    '''
    ret = []  # List of all cubic pregraphs that are obtained from g
    doub = []  # Potential double edges
    for u, v, _ in g.edges():
        if g.degree(u) < 3 and g.degree(v) < 3:
            doub.append((u, v))
    for eset in subsets(doub):
        # Not every choice of double edges is valid. If it is not a matching,
        # then there exists a vertex v that is incident with two double edges,
        # so d(v) >= 4.
        if not is_matching(eset):  
            continue
        h = Graph(g, multiedges=True, loops=True)
        for u, v in eset:
            h.add_edge((u, v))
        # At this point, the graph h contains double edges.
        for u in list(h):
            if h.degree(u) == 1:
                h.add_edge((u, u))
        # We added loops to graph h. No vertex may be incident with 2 semi-edges,
        # as the lifted graph wouldn't be simple. Therefore, a vertex of degree 1
        # must be augmented with a loop.
        
        # Since semi-edges are not supported by the Graph class, a vertex of
        # degree 2 always contains a semi-edge.
        if not contains_isomorphic(ret, h):
            ret.append(h)
    return ret

def relabel(pre):
    '''
    Relabel the vertices of a pregraph, so that vertices of the
    returned graph are labelled 0, 1, 2, ...
    '''
    rel = []
    mp = dict()
    n = 0
    for u in pre:
        for x in u:
            if x not in mp:
                mp[x] = n
                n += 1
        rel.append(tuple(mp[x] for x in u))
    return rel
        
def adj_matrix(pre):
    '''
    Assumes 0-based indices.
    '''
    n = max(max(u) for u in pre) + 1  # Determine the order of pregraph
    mat = [[0] * n for i in range(n)]
    for p in pre:
        if len(p) == 1:  # Semi-edge
            u, = p
            mat[u][u] += 1
        else:  # Proper edge (including loops)
            u, v = p
            mat[u][v] += 1
            mat[v][u] += 1
    return Matrix(mat)

def nonfirst_nonzero(mat):
    '''
    Return the list of indices of all entries which are non-zero
    and are not the first non-zero element in its row.
    '''
    pos = []
    n, m = mat.dimensions()
    for i in range(n):
        first = True
        for j in range(m):
            if mat[i, j] == 0:
                continue
            if not first:
                pos.append((i, j))
            first = False
    return pos

def all_matrices(mat):
    big_lst = []
    pos = nonfirst_nonzero(mat)  # The list of all positions where we may flip sign
    for chg in subsets(pos):
        m2 = Matrix(mat)
        for i, j in chg:
            m2[i, j] *= -1
        big_lst.append(m2)
    return big_lst

def disprove(pre, verbose=False):
    '''
    Return 0 if the pregraph can be "disproved" (i.e. it cannot given a nut graph).
    '''
    pre = relabel(pre)

    # BEGIN Pretest
    adj = adj_matrix(pre)
    ker = adj.right_kernel()
    if ker.dimension() > 1:
        # A zero entry can always be obtained somewhere. We can construct a
        # vector from the kernel of the covering graph that contains a 0 in the
        # entire orbit.
        return 0  # Disproved
    if ker.dimension() == 1:
        kev = ker.basis()[0]
        for x in kev:
            if x == 0:
                return 0  # Disproved (for the same reason as in the previous case)
    # END Pretest
    
    solutions = 0
    
    for M in all_matrices(adj):
        ker = M.right_kernel()
        if ker.rank() == 0:  # No solution
            continue

        lp = MixedIntegerLinearProgram(solver="GLPK")
        x = lp.new_variable(integer=True)  # x[1], x[2], x[3], ...
        basis = ker.basis()
        n = len(basis[0])
        for i in range(n):
            lp.add_constraint(sum(x[i + 1] * vec[i] for vec in basis) >= 1)
        lp.set_objective(0 * x[1])
        try:
            solution = lp.solve()
            solutions += 1
            vector = lp.get_values(x)
            print([vector[i + 1] for i in range(n)])
            if not verbose:
                return 1
        except sage.numerical.mip.MIPSolverException as e:
            assert e.args[0] == 'GLPK: Problem has no feasible solution'
            continue
    # TODO: Optimize for the final version. We can conclude that
    # it is not disproved as soon as we find the first solution.
    
    if solutions == 0:
        return 0  # Disproved (we couldn't find vector of magnitudes)
    else:
        return 1


if __name__ == '__main__':
    all_pre = []
    number_of_orbits = int(sys.argv[1])

    if number_of_orbits not in simple:
        print(f'Missing data: provide underlying graphs for {number_of_orbits} orbits')
        sys.exit(1)

    for g6str in simple[number_of_orbits]:
        for h in make_all_covers(Graph(g6str)):        
            all_pre.append(list((u, v) for u, v, _ in h.edges()) + list((u,) for u in h if h.degree(u) == 2))
            
    print(f'Number of pregraphs: {len(all_pre)}')

    bad_count = 0
    for pre in all_pre:
        has_solution = disprove(pre)
        if has_solution:
            print(pre)
        bad_count += has_solution
    print(f'Remaining cases: {bad_count}')


