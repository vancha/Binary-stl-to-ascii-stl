import sys

import struct
from struct import unpack

from Triangle import Triangle
from NormalVector import NormalVector
from Vertex import Vertex

'''
class that lets you convert binary stl to ascii stl, not to be used directly
'''
class stlReader:
    '''
    initializes stlReader with an stl file, loads stl file data to self
    '''
    def __init__(self, filename):
        if self.is_binary_stl(filename):
            self.read_binary_stl(filename)
        else:
            self.read_ascii_stl(filename)
    
    '''
    checks if the string filename points to a binary stl file
    '''
    def is_binary_stl(self, filename):
        with open(filename,'rb') as stl_file:
             return not b'solid' in stl_file.read(80)
    
    '''
    reads the file pointed to by filename as a binary stl file
    sets the following values:

        self.header                 the first 80 bytes of the stl file pointed to by filename
        self.number_of_triangles    the total number of triangles from the stl file pointed to by filename
        self.triangles              the array containing all number_of_triangles triangles from the stl file pointed to by filename
    '''
    def read_binary_stl(self, filename):

        with open(filename, 'rb') as stl_file:
            self.header                 = stl_file.read(80)
            self.number_of_triangles    = struct.unpack_from("<L",stl_file.read(4))[0]
            self.triangles              = []

            while True:
                try:
                    normal_vector           = NormalVector.from_bytes( stl_file.read(12) )
                    vertex_v1               = Vertex.from_bytes( stl_file.read(12) )
                    vertex_v2               = Vertex.from_bytes( stl_file.read(12) )
                    vertex_v3               = Vertex.from_bytes( stl_file.read(12) )
                    attribute_byte_count    = stl_file.read(2)

                    self.triangles.append( Triangle( normal_vector, [ vertex_v1, vertex_v2, vertex_v3 ] ))

                except struct.error:#this means we have read until the end of the binary file, we can likely safely break
                    break
    '''
    An ASCII stl file is structured like this:

    #Solid name
    #facet normal n1 n2 n3
    #    outer loop
    #        vertex v11, v12, v13
    #        vertex v21, v22, v23
    #        vertex v31, v32, v33
    #    endloop
    #endsolid name

    this function exports the read file as an ascii stl file, useful for conversion of binary stl to ascii stl
    '''
    def export_as_ascii_stl(self, destination_filename):
        with open(destination_filename, "w") as exported_file:
            exported_file.write("solid \n")
            for triangle in self.triangles:
                exported_file.write(triangle.to_ascii())
            exported_file.write("endsolid \n")

    '''
    This is a utility function, it exports the entire list of triangles as a list of points,which throws away 2 of the 3 vertices per triangle
    '''
    def as_point_list(self):
        point_list = []
        for triangle in self.triangles:
            point_list.append( triangle.vertices[0] )
        return point_list
    ''' 
    reads the file pointed to by filename as a ascii stl file
    sets the following values:

        self.header                 the first line of the stl file pointed to by filename
        self.triangles              the array containing all number_of_triangles triangles from the stl file pointed to by filename
    '''
    def read_ascii_stl(self, filename):
        with open(filename,'r') as stl_file:
            
            self.header = stl_file.readline()
            self.triangles = []
            
            while True:
                try:
                    _, _, x,y,z = stl_file.readline().strip().split(' ')#this line contains the normal
                    normal_vector = NormalVector(x,y,z)
                
                    _ = stl_file.readline()#ignore the next line, which has text `outer loop`
                
                    _, v1x, v1y, v1z = stl_file.readline().strip().split(' ')#get vertex 1 x, y and z
                    vertex_v1 = Vertex(v1x, v1y, v1z)
                
                    _, v2x, v2y, v2z = stl_file.readline().strip().split(' ')#get vertex 2 x, y and z
                    vertex_v2 = Vertex(v2x, v2y, v2z)
                
                    _, v3x, v3y, v3z = stl_file.readline().strip().split(' ')#get vertex 3 x, y and z
                    vertex_v3 = Vertex(v3x, v3y, v3z)
                
                    _ = stl_file.readline()#ignore the text `endloop`
                    _ = stl_file.readline()#ignore the text `endfacet`
                
                    self.triangles.append( Triangle(normal_vector, [vertex_v1, vertex_v2, vertex_v3] ) ) 
                except:
                    break
    '''
    this just stores one single vertex for every triangle in a pcd file. 
    '''
    def export_to_ascii_pcd(self,filename):
        with open(filename, 'w') as pcd_file:
            #writes the header for this pcd file
            pcd_file.write(f"VERSION .7\nFIELDS x y z\nSIZE 4 4 4\nTYPE F F F\nCOUNT 1 1 1\nWIDTH {len(self.triangles)}\nHEIGHT 1\nVIEWPOINT 0 0 0 1 0 0 0\nPOINTS {len(self.triangles)}\nDATA ascii\n")
            #loops over triangles
            for triangle in self.triangles:
                #writes only every first vertex of every triangle to the file
                pcd_file.write(f"{triangle.vertices[0].x} {triangle.vertices[0].y} {triangle.vertices[0].z}\n")
            
if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit('\nCall this file with two arguments:\n1:\tThe file to read\n2:\tThe file to export to')
    
    #the first argument is the file to read (can be binary stl or ascii stl) 
    binary_file_location    = sys.argv[1]
    #the second argument is the file to export to (can be stl or pcd)
    ascii_file_location     = sys.argv[2]
    
    #read the file
    stlreader               = stlReader( binary_file_location )

    #you can do the following things with this simple script:
    
    #export the loaded stl file as a pcd file (loses some data)
    stlreader.export_to_ascii_pcd( ascii_file_location )

    #export the loaded stl file as an ascii version of that stl file (useful for decoding binary to ascii stl)
    stlreader.export_as_ascii_stl( ascii_file_location )

    #just get the points from the stl file
    print(f'{stlreader.as_point_list()}')
