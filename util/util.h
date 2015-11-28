
/* 

This header is used for the importation of several miscellaneous macros, functions, typedefs, etc. 

*/

#pragma once

#ifndef UTIL_H
#define UTIL_H

#include <cassert>
#include <iostream>
#include <fstream>
#include <cstring>
#include <typeinfo>
#include <vector>
#include <cmath>
#include <chrono>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/dijkstra_shortest_paths.hpp>
#include <utility>
#include <algorithm>

using std::string;
using std::to_string;
using std::vector;
using std::cout;
using std::endl;

#define DEBUG BUILD_DEBUG
#define ASSERT(x, msg) if (DEBUG && !(x)) { fprintf(stderr, "Assertion failed in %s(%d): %s\n", __FILE__, __LINE__, msg); assert(false); exit(1); }

#define INT(x) ((int)(x))
#define DOUBLE(x) ((double)(x))
#define FLOAT(x) ((float)(x))
#define BYTE(x) ((unsigned char)(x))
#define SHORT(x) ((short)(x))
#define LONG(x) ((long)(x))
#define LONG_LONG(x) ((long long)(x))
#define U_LONG_LONG(x) ((unsigned long long)(x))

#define PI (3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709)

#define SQUARE(x) ((x)*(x))
#define MOD(a,b) (((INT(a)%INT(b))+INT(b))%INT(b))
#define MIN(a, b) ((a)<(b)?(a):(b))
#define MAX(a, b) ((a)>(b)?(a):(b))
#define IS_ODD(x) (MOD(x,2))
#define IS_EVEN(x) (!(MOD(x,2)))

#define QUIT exit(1);
#define TEST(x) cout << (#x) << ": " << x << endl;
#define PRINT(x) cout << x << endl;
#define DIVIDER cout << "======================================================================================================================================" << endl;
#define NEWLINE cout << endl;

#define IS_INT(a) same_type(a,INT(0))
#define IS_DOUBLE(a) same_type(a,DOUBLE(0))
#define IS_FLOAT(a) same_type(a,FLOAT(0))
#define IS_BYTE(a) same_type(a,BYTE(0))
#define IS_LONG(a) same_type(a,LONG(0))
#define IS_LONG_LONG(a) same_type(a,LONG_LONG(0))
#define IS_U_LONG_LONG(a) same_type(a,U_LONG_LONG(0))

typedef unsigned char byte;

template <class type1, class type2>
bool same_type(const type1 &a, const type2 &b) {
    return typeid(a) == typeid(b);
}

double G(const double &x, const double &sigma){
    return exp(-(x*x)/(2*SQUARE(sigma))) / sqrt(2*PI*SQUARE(sigma));
}

double G(const double &x, const double &y, const double &sigma){
    return exp(-(SQUARE(y)+SQUARE(x))/(2*SQUARE(sigma))) / (2*PI*SQUARE(sigma));
}

template <class real>
real lerp(const real &a, const real &b, const double &t) { // Linear Interpolation
    ASSERT(t>=0 && t<=1, (string("Interpolation factor (")+to_string(t)+") must be in interval [0.0,1.0]").c_str());
    return a*t+(1-t)*b;
}

/*  String Manipulation and File Reading */

void split(const string &line, const string &delimiter, vector<string> &vector_of_strings, bool skip_empty=false) {
    /* 
    Takes a string (line), a delimiter, vector of strings, and a skip_empty bool.
    Splits the string (line) everywhere the delimiter is found in the string (line) and puts all the new smaller substrings into the vector of strings. The substrings do not contain the delimiter.
    if skip_empty is false, our vector of strings will contain empty strings wherever there are two consecutive delimiters in the string (line). If skip_empty is true, our vector of strings will not contain any empty strings. 
    */
    auto start = 0U;
    auto end = line.find(delimiter);
    while (end != std::string::npos){
        if (!skip_empty || start != end) {
            vector_of_strings.push_back( line.substr(start, end - start) );
        } 
        start = end + delimiter.length();
        end = line.find(delimiter, start);
    }
    if (delimiter != string("\n")) { // since files have an extra newline at the end, we need to make sure we don't count the extra empty line we may get if our delimiter is the newline
        vector_of_strings.push_back( line.substr(start, end) );
    }
}

void write_file(const char* const &filename, string &input) { 
    std::ofstream out(filename);
    out << input;
    out.close();
}

void write_file(const string &filename, string &input) { 
    write_file(filename.c_str(), input);
}

void read_file(const char* const &filename, string &output) { 
    FILE* f = fopen(filename, "r");
    char* buffer;
    if (!f) {
        fprintf(stderr, "Unable to open %s for reading\n", filename);
        return;
    }
    
    fseek(f, 0, SEEK_END);
    int length = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    buffer = (char*)malloc(length+1);
    length = fread((void*)buffer, 1, length, f);
    fclose(f);
    buffer[length] = '\0';
    
    output = string(buffer);
    
    free(buffer);
}

void read_file(const string &filename, string &output) { 
    read_file(filename.c_str(), output);
}

void print_elapsed_time(const char* const &intro_text, const std::chrono::high_resolution_clock::time_point &start_time, const std::chrono::high_resolution_clock::time_point &end_time) {
    cout << intro_text << (std::chrono::duration_cast<std::chrono::nanoseconds>(end_time-start_time).count()) / (pow(10.0,9.0)) << " seconds." << endl;
}

template <class T>
void print_vector(const vector<T> &v) { 
    for(typename vector<T>::const_iterator it = v.begin(); it != v.end(); ++it) {
        cout << *it << endl;
    }
}

// BGL Helper Code

struct VertexProperties {
    int vertex_id;
//    string VertexStringProperty;
};

struct EdgeProperties {
    int edge_id;
//    string EdgeStringProperty;
};

typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS, VertexProperties, EdgeProperties, boost::vecS> Graph;
typedef Graph::vertex_descriptor vertex_descriptor;
typedef std::pair<Graph::edge_descriptor, bool> edge_pair;
typedef Graph::edge_descriptor edge_descriptor;

class Undirected_Graph { 
    public:
        Graph g;
        
        Undirected_Graph() {
        }
        
        void add_vertex(const int &id) {
            vertex_descriptor v = boost::add_vertex(g);
            g[v].vertex_id = id;
        }
        
        void add_edge_by_vertex_descriptor(const vertex_descriptor &v0, const vertex_descriptor &v1, const int &id) {
            edge_pair e = boost::add_edge(v0, v1, g); 
            g[e.first].edge_id = id;
        }
        
        void add_edge_by_vertex_id(const int &v0_id, const int &v1_id, const int &id) {
            add_edge_by_vertex_descriptor(get_vertex_by_id(v0_id), get_vertex_by_id(v1_id), id);
        }
        
        vertex_descriptor get_vertex_by_id(const int &id) {
            auto vertexIteratorRange = vertices(g);
            for(auto vertexIterator = vertexIteratorRange.first; vertexIterator != vertexIteratorRange.second; ++vertexIterator) {
                if (g[*vertexIterator].vertex_id == id) {
                    return *vertexIterator;
                }
            }
            cout << "Vertex ID (" << id << ") not found." << endl;
            QUIT;
        }
        
        edge_descriptor get_edge_by_id(const int &id) {
            auto edgeIteratorRange = edges(g);
            for(auto edgeIterator = edgeIteratorRange.first; edgeIterator != edgeIteratorRange.second; ++edgeIterator) {
                if (g[*edgeIterator].edge_id == id) {
                    return *edgeIterator;
                }
            }
            cout << "Edge ID (" << id << ") not found." << endl;
            QUIT;
        }
};

#endif // UTIL_H
