#ifndef RDF_H
#define RDF_H

#include "data_structure.h"

int nint(float x) {
   return floor(x+0.5);
}


int radial_distribution_function(FileInfo *vasprun, Configuration *config) {
   if (!config->rdf) {cout << "\nRDF called but not requested in configuration. Exiting"; return 1;}

   cout << "--- Starting Radial Distribution ---" <<endl;
   cout << "RDF requested for " << config->rdf_atoms.size() << " atom types: " << vec2str(config->rdf_atoms) << endl;
   //We need to use unwrapped coordinates.  Unwrap if not already unwrapped.
   vasprun->unwrap(); 
   
   //Start a simple bash script which calls GNUplot to plot the msd data
   ofstream of2;
   of2.open("output/plot_rdf.sh");
   of2 << "#!/bin/bash" << "\n" 
       << "gnuplot -persist << GNUPLOTINPUT" << "\n"
       << "set title \"Radial Distribution Function, g(r)\"\n"
       << "set term pdf\n"
       << "set output \"rdf.pdf\"\n"
       << "set xlabel \"r, Angstroms\"\n"
       << "set ylabel \"g(r)\"\n"
       << "plot ";

   //find the minimum cell dimension...we can't plot the RDF past half of this.
   double minimum_dimension = 10000000000000000;
   for (int i=0; i<3;i++) {
      if (vasprun->latt[i][i] < minimum_dimension) {
         minimum_dimension=vasprun->latt[i][i];
      }
   }

   //For each atom in the requested atom types
   for (int atomname=0; atomname < config->msd_atoms.size(); atomname++) {
      //this pointer will point to the atomType object for this type of atom 
      atomType* atomobject = vasprun->GetAtom(config->msd_atoms[atomname]);
      cout << "Beginning RDF calculation for " << atomobject->element << ".\n";   
      
      double rdf_sum=0; //the aggregate sum of of the displacements in the  timestep
      double xdist; // distances that the atom moved in x,y,z
      double ydist;
      double zdist;
      double xa,xb,ya,yb,za,zb;
      double distance;

      vector<double> bin_cutoff;
      
      int nbins = config->rdf_bins;
      vector<int> bins;
      //fill the bins vector with zeros
      for (int i=0;i<nbins;i++) {
         bins.push_back(0);
         bin_cutoff.push_back(i*minimum_dimension*0.5/nbins);
      }
      double bin_width = minimum_dimension*0.5/nbins;

      double xmin,ymin,zmin;
      double xmax,ymax,zmax;
      double sum_volume = 0;
      //for each timestep which we have positions for
      for (int t=1; t < atomobject->timesteps.size()-2; t++ ) {
         xmin,ymin,zmin = 100000000000;
         xmax,ymax,zmax = 0;
         //for each atom in the position vector of vectors
         for (int a=0; a<atomobject->atomspertype-1; a++) {
            xa = atomobject->timesteps[t].ppp[a][0];
            ya = atomobject->timesteps[t].ppp[a][1];
            za = atomobject->timesteps[t].ppp[a][2];
            //find the min/max coordinates for volume (density) calculation.
            if (xa > xmax) {xmax = xa;}
            if (ya > ymax) {ymax = ya;}
            if (za > zmax) {zmax = za;}
            if (xa < xmin) {xmin = xa;}
            if (ya < ymin) {ymin = ya;}
            if (za < zmin) {zmin = za;}

            for (int b=a+1; b<atomobject->atomspertype-1; b++ ) {
               xb = atomobject->timesteps[t].ppp[b][0];
               yb = atomobject->timesteps[t].ppp[b][1];
               zb = atomobject->timesteps[t].ppp[b][2];
               
               xdist = xb-xa;
               xdist = xdist - nint(xdist / vasprun->latt[0][0]) * vasprun->latt[0][0];
               ydist = yb-ya;
               ydist = ydist - nint(ydist / vasprun->latt[1][1]) * vasprun->latt[1][1];
               zdist = zb-za;
               zdist = zdist - nint(zdist / vasprun->latt[2][2]) * vasprun->latt[2][2];

               distance = sqrt(pow(xdist,2) + pow(ydist,2) + pow(zdist,2) );
               if (distance < (minimum_dimension) / 2.0) {
                  int binn = floor(distance * nbins / (minimum_dimension*0.5));
                  bins[binn]++;
               }
            }
         } 
         sum_volume+=(xmax-xmin)*(ymax-ymin)*(zmax-zmin); //volume taken by atoms this timestep
      }
  
   //write out the data for this element to an element-specific file
   ofstream of;
   of.open("output/" + config->rdf_data_prefix + atomobject->element + ".data");     
       
   //write out the gnuplot command, scaling the x-axis increment by the timestep to get it in picoseconds
   of2 << "'" << config->rdf_data_prefix + atomobject->element << ".data' with " << config->rdf_plot_type << " title '" << atomobject->element << "' , ";

   double fudge = 5.0;
   double atomic_density = fudge * atomobject->atomspertype / (sum_volume/atomobject->timesteps.size());
   //write each timestep to a file
   for (int n=0; n < nbins-1; n++) {
      double normalization = atomic_density / (4*3.14159264*bin_cutoff[n]*bin_cutoff[n]*bin_width*atomobject->timesteps.size() );
      of << bin_cutoff[n] << "\t" << bins[n]*normalization << "\n" ;
//      cout << bin_cutoff[n] << "\t" << bins[n]*normalization << "\n" ;
   }
   of.close();

   



   }

   //Close off the GNUPlot bash script
   of2 << "\nGNUPLOTINPUT\n";
   of2.close();

   //add a command to the global plot script to make the msd plots
   config->script_wrapper << "\nbash plot_rdf.sh \n" ;   

   return 0;

}

#endif