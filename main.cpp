
/*

TODO:

*/

#include <cstdio>
#include <cstdlib>
#include <cfloat>
#include <chrono>
#include "./util/util.h"

using std::cout;
using std::endl;
using std::string;

void usage() {
    fprintf(stderr, "usage: main\n");
    exit(1);
}

int main(int argc, char* argv[]) {
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    if (argc < 1) { 
        usage(); 
    }
    
    srand(std::time(0)); 
    
    ////////////////////////////////////////////////////////////////////////////////
    Undirected_Graph g; 
    g.add_vertex(11); 
    g.add_vertex(22); 
    g.add_vertex(33); 
    g.add_edge_by_vertex_id(22,33,111); 
    cout << g.get_edge_by_id(111) << endl; 
    cout << source(g.get_edge_by_id(111),g.g) << endl; 
    cout << target(g.get_edge_by_id(111),g.g) << endl; 
//    cout << g[0].vertex_id << endl; 
    g.get_vertex_by_id(22); 
    ////////////////////////////////////////////////////////////////////////////////
    
    auto end_time = std::chrono::high_resolution_clock::now();
    
    print_elapsed_time("Total Run Time: ", start_time, end_time);
    
    return 0;
}

