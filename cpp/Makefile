CC=g++
CFLAGS= -fmax-errors=3 -fopenmp

all: CFLAGS += -Wall -O3 -funroll-loops -DBUILD_DEBUG=0 -std=c++0x 
debug: CFLAGS += -g -Wall -DBUILD_DEBUG=1 -std=c++0x
all: LDFLAGS = -fopenmp 
debug: LDFLAGS = -fopenmp 

EXE=main
SRCS=main.cpp util.cpp
OBJS=$(SRCS:.cpp=.o)

all: $(SRCS) $(EXE)
debug: clean $(SRCS) $(EXE)

$(EXE): $(OBJS) 
	$(CC) $(CFLAGS) $(OBJS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) -c $< -o $@ 

clean:
	rm -f $(OBJS) $(EXE)

.PHONY: clean all debug
