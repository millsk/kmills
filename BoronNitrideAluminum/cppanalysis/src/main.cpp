#include "readXML.cpp"
#include "read_config.cpp"
#include "utility_functions.h"

#include "msd.h"


using namespace std;

int main() {
   cout << "\n Starting XML read"<<endl;
   FileInfo v;
   Configuration config;
   read_configfile(config);
   cout << "\n done"<<endl;

   v.input_filename="vasprun.xml";
   readXML(&v);


   if (config.msd) {
      msd(&v, &config);
   }


   return 0;
}



