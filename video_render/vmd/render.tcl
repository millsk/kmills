


   set skip 3

   # get the number of frames in the movie
   set num [molinfo top get numframes]
   # loop through the frames
   set count 0
   for {set i 0} {$i < $num} {incr i $skip} {
      # go to the given frame
      animate goto $i 
      # take the picture
      set filename pov_files/[format "%05d" $count].pov
      render POV3 $filename
      incr count 1
   }




