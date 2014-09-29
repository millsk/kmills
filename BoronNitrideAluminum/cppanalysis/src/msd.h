#ifndef MSD_H
#define MSD_H

#include "data_structure.h"

struct MsdStep {
   vector<double> msd_step;
   void declare(int len) {
       msd_step.clear();
       for (int i = 0; i < len; i ++) {
          msd_step.push_back(0);
       }
   }   
};



vector<double> msd_info; 


int msd(FileInfo *vasprun, Configuration *config) {
   if (!config->msd) {cout << "\nMSD called but not requested in configuration. Exiting"; return 1;}

   cout << "--- Starting Mean-Squared Displacement ---" <<endl;
   cout << "   " << "MSD requested for " << config->msd_atoms.size() << " atom types: " << vec2str(config->msd_atoms) << endl;

   
   vasprun->unwrap();
      
   vasprun->calculate_COM();    
   









   
   return 0;
   


}





#endif



