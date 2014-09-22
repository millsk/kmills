#ifndef MSD_H
#define MSD_H

#include "data_structure.h"



int msd(FileInfo *vasprun, Configuration *config) {
   if (!config->msd) {cout << "\nMSD called but not requested in configuration. Exiting"; return 1;}

   cout << "--- Starting Mean-Squared Displacement ---" <<endl;
   cout << "   " << "MSD requested for " << config->msd_atoms.size() << " atom types: " << vec2str(config->msd_atoms) << endl;

   
   vasprun->unwrap();
   





   
   return 0;
   


}





#endif



