#ifndef MSD_H
#define MSD_H

#include "data_structure.h"



vector<double> msd_info; 


int mean_square_displacement(FileInfo *vasprun, Configuration *config) {
   if (!config->msd) {cout << "\nMSD called but not requested in configuration. Exiting"; return 1;}

   cout << "--- Starting Mean-Squared Displacement ---" <<endl;
   cout << "   " << "MSD requested for " << config->msd_atoms.size() << " atom types: " << vec2str(config->msd_atoms) << endl;

   
   vasprun->unwrap(); 



   for (int atomname=0; atomname < config->msd_atoms.size(); atomname++) {
      //this object will hold the atomType object for this type of atom 
      atomType* atomobject = vasprun->GetAtom(config->msd_atoms[atomname]);
      //Calculate the center of mass for this atom_type. It'll be stored in the object.
      vasprun->calculate_COM(atomobject);
      //Make a pointer to the center of mass vector so I don't have to type so much all the time.
      vector<threevector>& COM = vasprun->atoms[atomobject->atomindex].COM.COM_value;         
      //for convenience, let i be the atomtype index, ie: vasprun->atoms[i] == atomobject (or at least should).
      int i = (atomobject->atomindex);



   

   
   vector<threevector>& test = vasprun->atoms[i].COM.COM_value;
   cout <<"   initial COM:  "   << test[0][0] << "\t" << test[0][1] << "\t" << test[0][2] << "\n" ;
}


   return 0;
   


}





#endif



