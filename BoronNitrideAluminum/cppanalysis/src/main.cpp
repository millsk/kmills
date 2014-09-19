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
      cout << "MSD requested for " << config.msd_atoms.size() << " atom types: " << vec2str(config.msd_atoms) << endl;;
   }


   return 0;
}



