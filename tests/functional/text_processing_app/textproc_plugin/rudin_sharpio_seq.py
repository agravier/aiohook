def a(n):
    """A014081"""
    # Indranil Ghosh, Jun 03 2017, https://oeis.org/A014081
    return sum([((n >> i) & 3 == 3) for i in range(len(bin(n)[2:]) - 1)])


def b(n):
    """A020985 but with 0 and 1"""
    return max(0, (-1) ** a(n))
