# makefile.txt, Geoffrey Weal, 31/5/23
SHELL = /bin/sh
CC    = g++
FLAGS        = -fPIC -std=c++20 -O3
LDFLAGS      = -shared
DEBUGFLAGS   = -O0 -D _DEBUG
RELEASEFLAGS = -O2 -D NDEBUG -combine -fwhole-program

TARGET  = KMC_algorithm.so
SOURCES = KMC_algorithm.cpp databases.cpp Initialisation_Methods/convert_arrays_to_unordered_maps.cpp Running_KMC_Methods/write_data_to_kMC_simTXT.cpp Running_KMC_Methods/write_data_to_kMC_sim_rate_constantsTXT.cpp Running_KMC_Methods/Auxiliary_Methods/auxillary_methods.cpp Running_KMC_Methods/print_time_passed.cpp Running_KMC_Methods/Rate_Constant_Methods/get_marcus_rate_constants_data.cpp Running_KMC_Methods/Rate_Constant_Methods/get_E_with_disorder.cpp Running_KMC_Methods/Rate_Constant_Methods/get_V_with_disorder.cpp Running_KMC_Methods/Rate_Constant_Methods/get_distance.cpp Running_KMC_Methods/get_probability_based_stepwise_diffusion_tensor.cpp

all: 
	rm -f $(TARGET)
	$(CC) $(FLAGS) $(LDFLAGS) -o $(TARGET) $(SOURCES)

clean: 
	rm -f $(TARGET)
