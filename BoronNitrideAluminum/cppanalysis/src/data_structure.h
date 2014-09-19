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
   int atomspertype, sindex, eindex;
   string element,pseudopotential;
   double mass, valence;
   std::vector<TimeStep> timesteps;

   atomType () {
      atomspertype=0; element="X  ";mass = 0.00; valence = 0.00; pseudopotential="garbage";
   }
}; 


struct FileInfo {
   //File input/output parameters
   string input_filename,output_data_location,system_name;
   //File data structures
   int numatoms,numtypes,ntimesteps;
   vector<int> atom_count;
   vector<double> latt_x,latt_y,latt_z;
   vector<atomType> atoms;
   vector<TimeStep> timesteps;
   double dt,starting_temperature; //timestep length, delta t

   int dataIntoAtoms(){
      for (unsigned i=0; i<atoms.size(); i++) {
         vector<TimeStep> alltimes;
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
   //returns a pointer to a specific atoms object, based on the passed element symbol
   //ie:   vasprun->GetAtom("Al")   returns a pointer the object holding the Aluminum atom info
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

struct Configuration {
  bool msd;
  string msd_outputfilename;
  string msd_atoms;
 
   
} config;




#endif


