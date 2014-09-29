#ifndef STORAGE_H_
#define STORAGE_H_

#include <string>
#include <vector>
#include <string.h>
#include <cmath>
using namespace std;

typedef vector<float> threevector;

struct TimeStep {
   vector<threevector> ppp;
   vector<threevector> ppp_uw; //unwrapped
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
   bool unwrapped_already=false;
   bool COM_already=false;
   vector<int> atom_count;
//   vector<double> latt_x,latt_y,latt_z;
   vector<threevector> latt;
   vector<threevector> COM; //centre of mass
   vector<atomType> atoms;
   vector<TimeStep> timesteps;
   float totalMass;
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

   int unwrap() {
      int sign;
      if (unwrapped_already) {return 0;}

      //copy the position vectors
      for (unsigned i=0; i<atoms.size(); i++) {  // for each atom type
         for (unsigned t=0; t < ntimesteps-1; t++) { //for each timestep
            atoms[i].timesteps[t].ppp_uw = atoms[i].timesteps[t].ppp;
         }
      }
      for (unsigned i=0; i<atoms.size(); i++) {  // for each atom type
         cout << "Unwrapping "<< atoms[i].element << " coordinates.\n";
         for (unsigned t=1; t < ntimesteps-1; t++) { //for each timestep
//            cout << "t=" <<  t << "\n";
//            atoms[i].timesteps[t].ppp_uw = atoms[i].timesteps[t].ppp;
            vector<threevector> &x0 = atoms[i].timesteps[t-1].ppp_uw;
            vector<threevector> &x1 = atoms[i].timesteps[t].ppp_uw;
            for (unsigned a=0; a<x0.size(); a++) { //for atom in ppp vector
               for (int x=0; x<3; x++) {  //for each dimension (0=x,1=y,2=z) {
                  if ((abs(x0[a][x] -x1[a][x])) > latt[x][x]/2 ) { //if the difference is greater than half lv
                     if (x0[a][x] < x1[a][x]) {sign=-1;} //if 
                     else {sign=1;}
                     x1[a][x] = x1[a][x] + sign*latt[x][x];
                  }
               }
            }
         }
      }
      unwrapped_already=true;
      return 0;
   }


   int mass_system(){
      for (unsigned i=0; i<atoms.size(); i++) {
         totalMass+=atoms[i].mass * atoms[i].atomspertype;
      }
      return 0;
   }


   int calculate_COM() {
      if (COM_already) {return 0;}
      mass_system();
      threevector thisCOM;
      thisCOM.push_back(0);
      thisCOM.push_back(0);
      thisCOM.push_back(0);
      for (unsigned t=0; t < ntimesteps-1; t++) { //for each timestep
         thisCOM[0] = 0; thisCOM[1]=0;thisCOM[2]=0;
         for (unsigned i=0; i<atoms.size(); i++) {  // for each atom type
            vector<threevector> &r = atoms[i].timesteps[t].ppp_uw;
            for (unsigned a=0; a<r.size(); a++) { //for atom in ppp vector
               for (int x=0; x<3; x++) {  //for each dimension (0=x,1=y,2=z) {
                  thisCOM[x] += (atoms[i].mass * r[a][x]);
               }
            }
         }
         thisCOM[0] /= totalMass;
         thisCOM[1] /= totalMass;
         thisCOM[2] /= totalMass;
         COM.push_back(thisCOM);
         if (t%10==0) {
            cout << COM[t][0] << "\t" << COM[t][1] << "\t" << COM[t][2] << "\n" ;
         }
      }
      COM_already=true;

         cout << "TOTAL MASS: " << totalMass << "\n";
//print it out to check:


   return 0;


   }
   




   FileInfo() {
      numatoms=0;
      input_filename = "/tmp/garbage";
      output_data_location = "/tmp/";
 
      /*latt_x.push_back(0);
      latt_x.push_back(0);
      latt_x.push_back(0);
      latt_y.push_back(0);
      latt_y.push_back(0);
      latt_y.push_back(0);
      latt_z.push_back(0);
      latt_z.push_back(0);
      latt_z.push_back(0);*/

   }
};

struct Configuration {
  bool msd;
  string msd_outputfilename;
  string tempstr;
  vector<string> msd_atoms;
   
} config;




#endif


