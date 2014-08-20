from ase import Atoms, Atom





def build_sheet(nx, nz):
    nx=nx+1
    nz=(nz+1)/2
    basic_cell= Atoms('C4', 
        positions=[[3.11488, 2.50000, 0.71000], 
               [4.34463, 2.50000, 1.42000], 
               [4.34463, 2.50000, 2.84000], 
               [3.11488, 2.50000, 3.55000]],
          cell=[[2.45951, 0, 0], 
                [0, 1, 0],
                [0, 0, 4.26]])
    atoms=basic_cell.repeat((nx,1,nz))
    atoms.pop(basic_cell.get_number_of_atoms()*nz-1)
    atoms.pop(0)
    return atoms

def nitrogenate(sheet, position):
    symbols = atoms.get_chemical_symbols()
    symbols[position] = 'N'
    sheet.set_chemical_symbols(symbols)
    return position

def daves_super_saturate(atoms):
    pos = atoms.get_positions()
    tree = KDTree(atoms.get_positions())
    list_tree = list(tree.query_pairs(1.430))
    bondedTo = [ [] for i in xrange(len(atoms))] 

    for bond in list_tree:
        bondedTo[bond[0]].append(bond[1])
        bondedTo[bond[1]].append(bond[0])

    Zs = atoms. get_atomic_numbers()
# figure out what needs a hydrogen atom
    for iatom in xrange(len(atoms)):
        nbonds = len( bondedTo[iatom] )
        Z = Zs[iatom]
        if (Z,nbonds) == (6,2):
            print "we should add H to atom ", iatom
            

            r0 = pos[iatom, :]
            bond1 = pos[ bondedTo[iatom][0] , : ] - r0
            bond2 = pos[ bondedTo[iatom][1],   :]  -r0
            rH = -(bond1 + bond2)
            rH = 1.09 * rH / np.linalg.norm(rH)
            atoms.append(Atom('H',  r0+rH ))

def find_edge_atoms(atoms):
    edge_atoms = []
    pos = atoms.get_positions()
    tree = KDTree(atoms.get_positions())
    list_tree = list(tree.query_pairs(1.430))
    bondedTo = [ [] for i in xrange(len(atoms))] 

    for bond in list_tree:
        bondedTo[bond[0]].append(bond[1])
        bondedTo[bond[1]].append(bond[0])

    Zs = atoms. get_atomic_numbers()
    # figure out what needs a hydrogen atom
    for iatom in xrange(len(atoms)):
        nbonds = len( bondedTo[iatom] )
        Z = Zs[iatom]
        if (Z,nbonds) == (6,2):
            edge_atoms.append(iatom)
    return edge_atoms
