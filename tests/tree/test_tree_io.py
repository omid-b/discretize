from __future__ import print_function
import numpy as np
import unittest
import os
import discretize

try:
    import vtk
except ImportError:
    has_vtk = False
else:
    has_vtk = True


class TestOcTreeMeshIO(unittest.TestCase):

    def setUp(self):
        h = np.ones(16)
        mesh = discretize.TreeMesh([h, 2*h, 3*h])
        cell_points = np.array([[0.5, 0.5, 0.5],
                                [0.5, 2.5, 0.5]])
        cell_levels = np.array([4, 4])
        mesh._insert_cells(cell_points, cell_levels)
        mesh.number()
        self.mesh = mesh

    def test_UBCfiles(self):

        mesh = self.mesh
        # Make a vector
        vec = np.arange(mesh.nC)
        # Write and read
        mesh.writeUBC('temp.msh', {'arange.txt': vec})
        meshUBC = discretize.TreeMesh.readUBC('temp.msh')
        vecUBC = meshUBC.readModelUBC('arange.txt')

        assert(mesh.nC == meshUBC.nC)
        assert mesh.__str__() == meshUBC.__str__()
        assert np.sum(mesh.gridCC - meshUBC.gridCC) == 0
        assert np.sum(vec - vecUBC) == 0
        assert np.all(np.array(mesh.h) - np.array(meshUBC.h) == 0)
        print('IO of UBC octree files is working')
        os.remove('temp.msh')
        os.remove('arange.txt')

    if has_vtk:
        def test_VTUfiles(self):
            mesh = self.mesh
            vec = np.arange(mesh.nC)
            mesh.writeVTK('temp.vtu', {'arange': vec})
            print('Writing of VTU files is working')
            os.remove('temp.vtu')


if __name__ == '__main__':
    unittest.main()
