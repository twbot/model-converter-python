#!/usr/bin/env python3

from .model import ModelParser, Exporter, Vertex, TexCoord, Normal, FaceVertex, Face
from functools import reduce

def is_obj(filename):
    return filename[-4:] == '.obj'

class OBJParser(ModelParser):

    def __init__(self):
        super().__init__()
        self.materials = []

    def parse_line(self, string):
        split = string.split(' ')
        first = split[0]
        split = split[1:]

        if first == 'usemtl':
            self.currentMaterial = split[0]
        elif first == 'v':
            self.add_vertex(Vertex().from_array(split))
        elif first == 'vn':
            self.add_normal(Normal().from_array(split))
        elif first == 'vt':
            self.add_tex_coord(TexCoord().from_array(split))
        elif first == 'f':
            splits = list(map(lambda x: x.split('/'), split))

            for i in range(len(splits)):
                for j in range(len(splits[i])):
                    if splits[i][j] is not '':
                        splits[i][j] = str(int(splits[i][j]) - 1)

            self.add_face(Face().from_array(splits))

class OBJExporter(Exporter):
    def __init__(self, model):
        super().__init__(model)

    def __str__(self):
        string = ""

        for vertex in self.model.vertices:
            string += "v " + ' '.join([vertex.x, vertex.y, vertex.z]) + "\n"

        string += "\n"

        if len(self.model.tex_coords) > 0:
            for tex_coord in self.model.tex_coords:
                string += "vt " + ' '.join([tex_coord.x, tex_coord.y]) + "\n"

            string += "\n"

        if len(self.model.normals) > 0:
            for normal in self.model.normals:
                string += "vn " + ' '.join([normal.x, normal.y, normal.z]) + "\n"

            string += "\n"

        for face in self.model.faces:
            string += "f "
            arr = []
            for v in [face.a, face.b, face.c]:
                sub_arr = []
                sub_arr.append(str(int(v.vertex) + 1))
                if v.normal is None:
                    if v.texture is not None:
                        sub_arr.append('')
                        sub_arr.append(str(int(v.texture) + 1))
                elif v.texture is not None:
                    sub_arr.append(str(int(v.texture) + 1))
                    if v.normal is not None:
                        sub_arr.append(str(int(v.normal) + 1))
                arr.append('/'.join(sub_arr))

            string += ' '.join(arr) + '\n'
        return string
