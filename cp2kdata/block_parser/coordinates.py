import regex as re
import numpy as np

INIT_ATOMIC_COORDINATES_RE = re.compile(
    r"""
    \sMODULE\sQUICKSTEP:\s\sATOMIC\sCOORDINATES\sIN\sangstrom\s*\n
    \n
    \s+Atom\s+Kind\s+Element\s+X\s+Y\s+Z\s+Z\(eff\)\s+Mass\s*\n
    \n
    (
        \s+(?P<atom>\d+)
        \s+(?P<kind>\d+)
        \s+(?P<element>\w+)
        \s+\d+
        \s+(?P<x>[\s-]\d+\.\d+)
        \s+(?P<y>[\s-]\d+\.\d+)
        \s+(?P<z>[\s-]\d+\.\d+)
        \s+[\s-]\d+\.\d+
        \s+[\s-]\d+\.\d+
        \n
    )+
    """,
    re.VERBOSE
)


def parse_init_atomic_coordinates(output_file):
    init_atomic_coordinates = []
    atom_kind_list = []
    chemical_symbols = []
    for match in INIT_ATOMIC_COORDINATES_RE.finditer(output_file):
        for x, y, z in zip(*match.captures("x", "y", "z")):
            init_atomic_coordinates.append([x, y, z])
        atom_kind_list = [int(kind) for kind in match.captures("kind")]
        chemical_symbols = match.captures("element")
    if init_atomic_coordinates:
        return np.array(init_atomic_coordinates, dtype=float), np.array(atom_kind_list, dtype=int), chemical_symbols
    else:
        return None
