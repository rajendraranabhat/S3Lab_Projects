
clear all;

%files--> caso_I.mat, caso_II.mat, caso_III.mat, caso_base.mat
%addpath ../data

load data/caso_I.mat; %ccarga, demcli, pc

nRows = size(demcli,1); %85
nCols = size(demcli,2); %6

isEmptyCell = cellfun(@isempty, demcli);%returns 0,1 matrix(85 by 6)

[nCellRows, nCellCols] = cellfun(@size, demcli); %shape of individual cell
totalRows = sum(cellfun(@length, demcli)(:)); %Total rows of cells
totalCols = unique(nCellCols)(2);  %column of cell

demcliMat =  []; %zeros(totalRows,totalCols); %Holder of the cell data.
pc_col = 1;
%iterate all the cell
for i=1:nRows  %85
  for j = 1:2:nCols %since 1,3,5 only contains data   
    pc_col = mapPC2DemcliCol(j);  
    %fprintf('%i\n %i\n %i\n', i,j,pc_col);
    if(!isEmptyCell(i,j))        
        demcliMat = [demcliMat; demcli{i,j}, pc{i,pc_col}];
    end       
  end
end

%saves the file into demcliMat.mat
save demcliMat.mat demcliMat

