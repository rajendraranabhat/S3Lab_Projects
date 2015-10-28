
%Function mapping from Demcli Column to pc column.
function pc_col = mapPC2DemcliCol(demcliCol)
   
   pc_col = 0;  
   if(demcliCol == 1)
      pc_col = 1;
   end
   if(demcliCol == 3)
      pc_col = 2;
   end
   if(demcliCol == 5)
      pc_col = 3;
   end   
end
