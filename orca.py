from ase import Atoms, Atom






def make_orca(atoms, filename="filename.inp", charge="0", multiplicity="1", method="am1"):
    # if sum(atoms.get_atomic_numbers()) % 2 == 1:
    #        spin= "! HF"
    # elif sum(atoms.get_atomic_numbers()) % 2 == 0:
    #        spin= "! UHF"
    out=''
    parameters0= '{0}\t{1}\t{2}\n{3}\n'.format("%method", "method", method, "end")
    parameters1='{0}\t{1}\t{2}\t{3}\n'.format("*", "xyz", charge, multiplicity)
    out=out+parameters0+parameters1
    end_of_atom_coordinates="*"
    with open(filename, 'w') as f:
        f.write(out)
        f.write(print_atoms(atoms))
        f.write(end_of_atom_coordinates)
    subprocess.call("/home/matthew/orca/orca "+ filename + " > temp.out", shell=True)
    return parse("temp.out")

def print_atoms(atoms):
    out=''
    for atom in atoms:
        atom_str= '{0}\t{1}\t{2}\t{3}\n'.format(atom.symbol, atom.position[0], atom.position[1], atom.position[2])
        out=out+atom_str
    return out

def parse(filename):
    myfile= ccopen(filename)
    data = myfile.parse()
    return data

