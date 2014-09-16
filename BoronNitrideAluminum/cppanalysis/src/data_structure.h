#ifndef STORAGE_H_
#define STORAGE_H_

#include <string>
#include <vector>
#include <string.h>
using namespace std;

typedef vector<float> threevector;

struct TimeStep {
   vector<threevector> ppp;
   vector<threevector> fff;
};


struct atomType {
   int atomspertype;
   string element;
   int sindex;
   int eindex;
   double mass;
   double valence;
   string pseudopotential;
   std::vector<TimeStep> timesteps;

/*&   void dataToAtomType(TimeStep* d) {
      cout << "!!!!! " << d->ppp.size() << endl;
   } */

   atomType () {
      atomspertype=0; element="X  ";mass = 0.00; valence = 0.00; pseudopotential="garbage";
   }




}; 


struct FileInfo {
   //File input/output parameters
   std::string input_filename;
   std::string output_data_location;
   //File data structures
   int numatoms;
   int numtypes;
   int ntimesteps;
   std::vector<int> atom_count;
   vector<double> latt_x;
   vector<double> latt_y;
   vector<double> latt_z;
   std::vector<atomType> atoms;
   std::vector<TimeStep> timesteps;

   int dataIntoAtoms(){
      for (unsigned i=0; i<atoms.size(); i++) {
         std::vector<TimeStep> alltimes;
         for (unsigned t=0;t<ntimesteps-1; t++) {
            TimeStep ts;
            for (unsigned a=atoms[i].sindex;a<atoms[i].eindex; a++) {
               ts.ppp.push_back(timesteps[t].ppp[a] ) ;
               ts.fff.push_back(timesteps[t].fff[a] ) ;
            }
            alltimes.push_back(ts);
         }
         atoms[i].timesteps = alltimes;
      }
      return 1;
   }

   
   atomType* GetAtom(string element) {
      for (unsigned i=0; i<atoms.size(); i++) {
         if (atoms[i].element==element) {
            return &atoms[i];
         }
      }
      //If the function hasn't returned yet, then the atom type was not found. Kill the program since
      //we'll later get a Segmentation Fault for pointing to a non-existent object.
      cout << endl << endl << "FATAL ERROR!!!" <<endl<< "ATOM TYPE "<<element<<" NOT FOUND. EXITING." << endl;
      exit(0);
   }


   FileInfo() {
      numatoms=0;
      input_filename = "/tmp/garbage";
      output_data_location = "/tmp/";
 
      latt_x.push_back(0);
      latt_x.push_back(0);
      latt_x.push_back(0);
      latt_y.push_back(0);
      latt_y.push_back(0);
      latt_y.push_back(0);
      latt_z.push_back(0);
      latt_z.push_back(0);
      latt_z.push_back(0);

   }
};

   




#endif


