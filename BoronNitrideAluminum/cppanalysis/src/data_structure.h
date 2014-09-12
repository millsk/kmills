#ifndef STORAGE_H_
#define STORAGE_H_

#include <string>
#include <vector>
using namespace std;

struct atomType {
   int atomspertype;
   string element;
   double mass;
   double valence;
   string pseudopotential;
};



struct FileInfo {
   //File input/output parameters
   std::string input_filename;
   std::string output_data_location;
   //File data structures
   int numatoms;
   int numtypes;
   std::vector<int> atom_count;

   std::vector<atomType> atom_types;

   FileInfo() {
      numatoms=0;
      input_filename = "/tmp/garbage";
      output_data_location = "/tmp/";
   }
};






#endif


