#include "readXML.cpp"
#include "read_config.cpp"
#include "utility_functions.h"



using namespace std;

int main() {
   cout << "\n Starting XML read"<<endl;
   FileInfo v;
   v.input_filename="vasprun.xml";
   Configuration config;
   read_configfile(config);
   readXML(&v);
   cout << "\n done"<<endl;

   if (config.msd) {
      vector<string> msd_atoms = string_split_to_vector(config.msd_atoms);
      for (int i=0; i<msd_atoms.size()-1; i++) {
         cout << msd_atoms[i] <<endl;
      }
   }


   return 0;
}



