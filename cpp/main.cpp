
/*

TODO:
    More Important:
        Finish Host class
        
    Less Important:
        Look into more compile options to make the code run faster. Stick it in the Makefile
*/

#include "util.h"

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
    PRINT("WOO!")
    ////////////////////////////////////////////////////////////////////////////////
    
    auto end_time = std::chrono::high_resolution_clock::now();
    
    print_elapsed_time("Total Run Time: ", start_time, end_time);
    
    return 0;
}

