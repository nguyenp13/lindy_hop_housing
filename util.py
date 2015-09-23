
import sys
import os
import ntpath
import math
import pdb
import random
import string

def remove_file_extension(file_name):
    index_of_last_dot = file_name.rfind('.')
    return file_name if index_of_last_dot == -1 else file_name[:index_of_last_dot]

def generate_unique_file_name(extension0, placement_directory='.'):
    extension = extension0.replace('.','')
    new_file_name = None
    file_exists = True
    while file_exists:
        length_of_file_name = max(10,random.randint(0,255)-len(extension)-1) # the minus 1 is for the '.'
        new_file_name = ''.join([random.choice(string.ascii_letters) for i in xrange(length_of_file_name)])+'.'+extension
        file_exists = os.path.exists(os.path.join(placement_directory,new_file_name))
    return new_file_name

def generate_unique_directory_name(placement_directory='.'):
    new_directory_name = None
    directory_exists = True
    while directory_exists:
        length_of_directory_name = random.randint(10,255) 
        new_directory_name = ''.join([random.choice(string.ascii_letters) for i in xrange(length_of_directory_name)])
        directory_exists = os.path.exists(os.path.join(placement_directory,new_directory_name))
    return new_directory_name

def assertion(condition, message, error_code=1):
    if not condition:
        print >> sys.stderr, ''
        print >> sys.stderr, message
        print >> sys.stderr, ''
        sys.exit(error_code)

'''
class Graph(object):
    def __init__(self, vertices0=[], edges0=[]):
        self.vertices = set(vertices0) # is a set of strings that act as node labels
        self.edges = set([frozenset(e) for e in edges0]) # is a set of edges, which are sets of two strings that are vertex labels

    def get_vertices(self):
        return self.vertices

    def get_edges(self):
        return self.edges

    def add_vertex(self, vertex):
        vertices.add(vertex)
    
    def add_edge(self, edge0):
        edge = frozenset(edge0)
        assertion(len(edge)==2, "edge type error: edge is not of size 2")
        self.edges.add(edge)

    def __repr__(self):
        res = __file__[:-2]
        res += "Graph("
        res += str(list(self.vertices))
        res += ", "
        res += str([list(f) for f in self.edges])
        res += ")"
        return res
    
    def __str__(self):
        res = "vertices: "
        res += str(list(self.vertices))
        res += "\n"
        res += "edges: "
        res += str([list(f) for f in self.edges])
        return res
'''

