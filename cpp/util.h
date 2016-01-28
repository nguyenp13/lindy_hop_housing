
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

/* Types */

template <class type1, class type2>
bool same_type(const type1 &a, const type2 &b) {
    return typeid(a) == typeid(b);
}

/* Math */

template <class real>
real lerp(const real &a, const real &b, const double &t) { // Linear Interpolation
    ASSERT(t>=0 && t<=1, (string("Interpolation factor (")+to_string(t)+") must be in interval [0.0,1.0]").c_str());
    return a*t+(1-t)*b;
}

double G(const double &x, const double &sigma);
double G(const double &x, const double &y, const double &sigma);

/*  String Manipulation and File Reading */

void split(const string &line, const string &delimiter, vector<string> &vector_of_strings, bool skip_empty=false);
void write_file(const char* const &filename, string &input);
void write_file(const string &filename, string &input);
void read_file(const char* const &filename, string &output);
void read_file(const string &filename, string &output);
void print_elapsed_time(const char* const &intro_text, const std::chrono::high_resolution_clock::time_point &start_time, const std::chrono::high_resolution_clock::time_point &end_time);

/* Pretty Printing */

template <class T>
void print_vector(const vector<T> &v) { 
    for(typename vector<T>::const_iterator it = v.begin(); it != v.end(); ++it) {
        cout << *it << endl;
    }
}

#endif // UTIL_H
