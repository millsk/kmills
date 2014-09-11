#ifndef STORAGE_H_
#define STORAGE_H_

#include <string>
#include <vector>


struct FileInfo {
   //File input/output parameters
   std::string input_filename;
   std::string output_data_location;
   //File data structures
   std::vector<string> atom_types;
   std::vector<int> atom_count;

   FileInfo() {
      input_filename = "/tmp/garbage";
      output_data_location = "/tmp/";
   }
};




#endif












#endif
