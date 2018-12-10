import numpy as np

BOHR2ANG = 0.52917721067
ANG2BOHR = 1.889726125457828


def parse_xyz_str(xyz_str, ang2bohr=False):
    """Parse a xyz string.

    Paramters
    ---------
    xyz_str : str
        The contents of a .xyz file.
    with_comment : bool
        Return comment line if True.

    Returns
    -------
    atoms : list
        List of length N (N = number of atoms) holding the
        element symbols.
    coords: np.array
        An array of shape (N, 3) holding the xyz coordinates.
    comment_line : str, optional
        Comment line if with_comment argument was True.
    """

    xyz_lines = xyz_str.strip().split("\n")
    atom_num = int(xyz_lines[0].strip())
    comment_line = xyz_lines[1]

    # Only consider the first four items on a line
    atoms_coords = [line.strip().split()[:4]
                    for line in xyz_str.strip().split("\n")[2:]
    ]
    atoms, coords = zip(*[(a, c) for a, *c in atoms_coords])
    coords = np.array(coords, dtype=np.float)
    if ang2bohr:
        coords *= ANG2BOHR
    return atoms, coords


def parse_xyz_file(xyz_fn, ang2bohr=False):
    with open(xyz_fn) as handle:
        xyz_str = handle.read()

    return parse_xyz_str(xyz_str, ang2bohr)
