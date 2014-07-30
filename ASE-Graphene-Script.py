# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from ase import Atoms
from ase.visualize import view
import numpy as np
from cclib.parser import ccopen
from cclib.parser import ORCA
import logging
from scipy.spatial import KDTree
from collections import Counter


np.set_printoptions(precision=3,suppress=True)

def build_sheet(nx, nz='nx'):
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
    
def print_atoms(atoms):
    out=''
    for atom in atoms:
        atom_str= '{0}\t{1}\t{2}\t{3}\n'.format(atom.symbol, atom.position[0], atom.position[1], atom.position[2])
        out=out+atom_str
    return out

def make_orca(filename="filename.inp", charge="0", multiplicity="2", method="am1"):
    # if sum(atoms.get_atomic_numbers()) % 2 == 1:
    #        spin= "! HF"
    # elif sum(atoms.get_atomic_numbers()) % 2 == 0:
    #        spin= "! UHF"

    out=''
    parameters0= '{0}\t{1}\t{2}\n{3}\n'.format("%method", "method", method, "end")
    parameters1='{0}\t{1}\t{2}\t{3}\n'.format("*", "xyz", charge, multiplicity)
    out=out+parameters0+parameters1
    end_of_atom_coordinates="*"
    with open(filename, 'a+') as f:
        f.write(out)
        f.write(print_atoms(atoms))
        f.write(end_of_atom_coordinates)


    
def parse(filename, cclib_attribute):
    myfile= ccopen(filename)
    data = myfile.parse()
    data.cclib_attribute

def count_bonded_adj_atoms(atoms):
    bonded_3, bonded_2 = ([] for i in range(2))
    bonded_3_atoms = np.array(bonded_3)
    bonded_2_atoms = np.array(bonded_2)
    tree = KDTree(atoms.get_positions())
    list_tree = list(tree.query_pairs(1.430))
    dictionary_count=Counter(elem[0] for elem in list_tree) + Counter(elem[1] for elem in list_tree)
    for k, v in dictionary_count.iteritems():
        if v == 3:
            bonded_3_atoms = np.append(bonded_3_atoms, k)
        elif v == 2:
            bonded_2_atoms = np.append(bonded_2_atoms, k)
        else:
            pass
    print "Index bonded to 3 atoms", 
    print bonded_3_atoms
    print "Index bonded to 2 atoms",
    print bonded_2_atoms
    


    
atoms=build_sheet(3,3)
nitrogenate(atoms, 0)
#make_orca()
#view(atoms, viewer='avogadro')
count_bonded_adj_atoms(atoms)

# <codecell>

