#ifndef MSD_H
#define MSD_H

#include "data_structure.h"

int mean_square_displacement(FileInfo *vasprun, Configuration *config) {
   if (!config->msd) {cout << "\nMSD called but not requested in configuration. Exiting"; return 1;}

   cout << "--- Starting Mean-Squared Displacement ---" <<endl;
   cout << "MSD requested for " << config->msd_atoms.size() << " atom types: " << vec2str(config->msd_atoms) << endl;

   
   vasprun->unwrap(); 

   ofstream of2;
   of2.open("output/plot_msd.sh");
   of2 << "#!/bin/bash" << "\n" 
       << "gnuplot -persist << GNUPLOTINPUT" << "\n"
       << "set title \"Mean Square Displacement\"\n"
       << "set term pdf\n"
       << "set output \"msd.pdf\"\n"
       << "set xlabel \"Time, picoseconds\"\n"
       << "set ylabel \"distance, Angstroms\"\n"
       << "unset key" << "\n"
       <<"plot ";

   for (int atomname=0; atomname < config->msd_atoms.size(); atomname++) {
      //this object will hold the atomType object for this type of atom 
      atomType* atomobject = vasprun->GetAtom(config->msd_atoms[atomname]);
      //Calculate the center of mass for this atom_type. It'll be stored in the object.
      vasprun->calculate_COM(atomobject);
      //Make a pointer to the center of mass vector so I don't have to type so much all the time.
      vector<threevector>& COM = vasprun->atoms[atomobject->atomindex].COM.COM_value;         
      //for convenience, let i be the atomtype index, ie: vasprun->atoms[i] == atomobject (or at least should).
      int i = (atomobject->atomindex);
      
      int msd_count=0;
      double msd_sum=0;
      double xdist;
      double ydist;
      double zdist;
      for (int t=1; t < atomobject->timesteps.size()-2; t++ ) {
         for (int a=0; a<atomobject->atomspertype-1; a++) {
//            for (int t2=t+1; t2 < atomobject->timesteps.size()-1; t2++ ) {
               int t2=0;
               xdist = atomobject->timesteps[t].ppp_uw[a][0] - atomobject->timesteps[t2].ppp_uw[a][0]
                       - atomobject->COM.COM_value[t][0] + atomobject->COM.COM_value[t2][0];
               ydist = atomobject->timesteps[t].ppp_uw[a][1] - atomobject->timesteps[t2].ppp_uw[a][1]
                       - atomobject->COM.COM_value[t][1] + atomobject->COM.COM_value[t2][1];
               zdist = atomobject->timesteps[t].ppp_uw[a][2] - atomobject->timesteps[t2].ppp_uw[a][2]
                       - atomobject->COM.COM_value[t][2] + atomobject->COM.COM_value[t2][2];
               msd_sum+=pow(xdist,2) + pow(ydist,2) + pow(zdist,2);
               msd_count++;
//            }
         }
         atomobject->MSD.msd_value.push_back(sqrt( msd_sum / msd_count ));
         msd_sum=0;
         msd_count=0;
      }


   ofstream of;
   of.open("output/msd_" + atomobject->element + ".data");
       
       
       

   of2 << " 'msd_" << atomobject->element << ".data' using (\\$0*" << vasprun->dt << "*0.001):1 with lines, ";


   for (int line=0; line < atomobject->MSD.msd_value.size(); line++) {
      of << atomobject->MSD.msd_value[line] << "\n" ;
   }
   of.close();

   
   vector<threevector>& test = vasprun->atoms[i].COM.COM_value;
   cout <<"   initial COM:  "   << test[0][0] << "\t" << test[0][1] << "\t" << test[0][2] << "\n" ;
}

   of2 << "\nGNUPLOTINPUT\n";
   of2.close();

   config->script_wrapper << "\nbash plot_msd.sh \n" ;   


   return 0;
   


}





#endif



