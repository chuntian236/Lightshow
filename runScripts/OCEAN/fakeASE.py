# coding: latin-1
# J Vinson, 2020

""" Reads/write OCEAN files
"""
from ase.atoms import Atoms
#from collections import OrderedDict
import os
import sys
from ase.units import Bohr


def write_ocean_in( filename: str, atoms: Atoms, input_data: dict ):

    filename = os.path.expanduser(filename)
    mode = 'w'
    fd = open(filename, mode)

    input_data_str = []
    for key in input_data:
      input_data_str.append( str(key) + ' { ' + str(input_data[key]) + ' }\n' )

    fd.write( ''.join(input_data_str ))

    if any(atoms.get_initial_magnetic_moments()):
        raise NameError( 'Spin=2 not implemented yet' )

#    atomic_species = OrderedDict()
#    atomic_species_str = []    
#    znucl = []
#    typat = []
    
#    ispecies = 0

#    for atom in atoms:
#        if atom.symbol not in atomic_species:
#            ispecies += 1
#            atomic_species[atom.symbol] = ispecies  # just a placeholder
#  
#        znucl.append( str( atom.numbers ) + ' ' )
#        typat.append( str( atomic_species[atom.symbol] ) + ' ' )
#        atomic_positions_str.append( '{coords[0]:.10f} {coords[1]:.10f} {coords[2]:.10f}\n'.format(
#              coords=[atom.a, atom.b, atom.c] ))


    species = sorted(set(atoms.numbers))
    fd.write('znucl {{ {} }}\n'.format(' '.join(str(Z) for Z in species)))
    fd.write('typat')
    fd.write('{\n')
    types = []
    for Z in atoms.numbers:
        for n, Zs in enumerate(species):
            if Z == Zs:
                types.append(n + 1)
    n_entries_int = 20  # integer entries per line
    for n, type in enumerate(types):
        fd.write(' %d' % (type))
        if n > 1 and ((n % n_entries_int) == 1):
            fd.write('\n')
    fd.write(' }\n')

    atomic_positions_str = []
    for atom in atoms:
        atomic_positions_str.append( '{coords[0]:.10f} {coords[1]:.10f} {coords[2]:.10f}\n'.format(
              coords=[atom.a, atom.b, atom.c] ))

    fd.write( 'xred {\n' )
    fd.write( ''.join(atomic_positions_str))
    fd.write( '}\n' )

    fd.write( 'acell {{ {acell[0]} {acell[0]} {acell[0]} }} \n'.format( acell=[1/Bohr] ) )
    
    fd.write( 'rprim {{ {cell[0][0]:.14f} {cell[0][1]:.14f} {cell[0][2]:.14f}\n'
              '        {cell[1][0]:.14f} {cell[1][1]:.14f} {cell[1][2]:.14f}\n'
              '        {cell[2][0]:.14f} {cell[2][1]:.14f} {cell[2][2]:.14f}  }}\n'
                   ''.format(cell=atoms.cell))

