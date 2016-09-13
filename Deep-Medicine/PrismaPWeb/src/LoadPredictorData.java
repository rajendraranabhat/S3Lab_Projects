import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.sql.DriverManager;
import java.sql.SQLException;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;


public class LoadPredictorData {
	static Connection con=null;
	
	
	public static void main(String[] args) throws Exception {
		LoadPredictorData lpd=new LoadPredictorData();
		createConnection();
		String directory="/home/rbhat/Bishal/Web Application/Web Application/data";
		String datafile="data.csv";
		String idfile="id_acc.csv";
		String[] outputFiles={"output_cv_comp_new_subset.csv","output_ICU_comp_subset.csv","output_mort_status_30d_subset.csv","output_mv_comp_subset.csv","output_rifle7_subset.csv","output_sevsep_3new_subset.csv"};
		String[] outputNames={"cardioVascular","ICU","mortality","ventilator","rifle7","sepsis"};
		lpd.id_acct_map(directory, idfile);
		String[] header=lpd.loadData(directory, datafile);
		lpd.load_output_values(directory, outputFiles, outputNames,header);
		lpd.load_idList(directory, "dataSet.csv");
		con.close();
	}
	
	
	static void createConnection() throws ClassNotFoundException, SQLException{
		Class.forName("com.mysql.jdbc.Driver");
		//con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "panda", "shands@UF");
		con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "root", "");
	}
	
	String[] loadData(String directory, String file) throws Exception{
		System.out.println("Creating table to enter data...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table patientDetails(id varchar(50),feature varchar(50),value varchar(50))";
		String createTempTable="create table patientTempDetails(id varchar(50),feature varchar(50),value varchar(50))";
		String createIndex="create index patientDetailsIndex on patientDetails (id,feature)";
		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table patientDetails");
			stmt.execute(createTable);
		}
		
		try{
			stmt.execute(createTempTable);
		}catch(Exception ex){
			stmt.execute("drop table patientTempDetails");
			stmt.execute(createTempTable);
		}
		System.out.println("Table created to enter data...");
		
		System.out.println("Reading output file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String[] header=br.readLine().split(",");
	    
	    String line;
	    int i=0;
	    StringBuilder sqlValues=new StringBuilder();
	    
	    while((line=br.readLine())!=null){
			if(i==0)
		    	sqlValues=new StringBuilder("insert into patientTempDetails values");
		    	
    		String[] strArr=line.split(",");

    		for(int j=1;j<header.length;j++){
        		if(header[j].equalsIgnoreCase("MDC"))
        			strArr[j]=strArr[j].toLowerCase().trim().split(" ")[0];
        		if(strArr[j].toLowerCase().trim().equals("er"))
        			sqlValues.append("(\""+strArr[0].trim()+"\",\""+header[j].toLowerCase().trim()+"\",\""+strArr[j].trim()+"\"),");
        		else
        			sqlValues.append("(\""+strArr[0].trim()+"\",\""+header[j].toLowerCase().trim()+"\",\""+strArr[j].toLowerCase().trim()+"\"),");
    		}
    		i++;
    		
    		if(i>500){
    			i=0;
    			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
    		}    		
   		}
		if(i!=0)
			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    stmt.execute("insert into patientDetails select map.accountNo, temp.feature, temp.value from idMap map,patientTempDetails temp where temp.id=map.id");
	    stmt.execute("drop table patientTempDetails");
	    System.out.println("All Data of patients are entered...");
	    
	    System.out.println("Creating Index on the data of Patients");
		try{
			stmt.execute(createIndex);
		}catch(Exception ex){
			stmt.execute("alter table patientDetails drop index patientDetailsIndex");
			stmt.execute(createIndex);
		}
	    System.out.println("The index is created...");
	   
	    return header;
	}

	void id_acct_map(String directory, String file) throws Exception{
		System.out.println("Creating table to enter ID v/s Account Number data...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table idMap(id varchar(50), accountNo varchar(50))";
		String createIndex="create index idMapIndex on idMap(id)";
		String createTableID="create table idList(id varchar(50))";
		String createIndexID="create index idListIndex on idList(id)";
		//
		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table idMap");
			stmt.execute(createTable);
		}
		
		try{
			stmt.execute(createTableID);
		}catch(Exception ex){
			stmt.execute("drop table idList");
			stmt.execute(createTableID);
		}
		System.out.println("Table created to enter ID v/s Account Number...");
		
		System.out.println("Reading id Map file...");
		System.out.println((directory));
		System.out.println((file));
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    br.readLine();
	    
	    StringBuilder sqlValues=new StringBuilder();
	    int i=0;
	    while((line=br.readLine())!=null){
			if(i==0)
		    	sqlValues=new StringBuilder("insert into idMap values");
		    	
    		String[] strArr=line.split(";");
    		sqlValues.append("(\""+strArr[0].trim()+"\",\""+strArr[1].trim()+"\"),");
    		i++;
    		
    		if(i>500){
    			i=0;
    			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
    		}    		
   		}
		if(i!=0)
			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    System.out.println("All Data of ID v/s Account Number are entered...");
	    
	    System.out.println("Creating Index on the data of ID v/s Account Number");
		try{
			stmt.execute(createIndex);
		}catch(Exception ex){
			stmt.execute("alter table idMap drop index idMapIndex");
			stmt.execute(createIndex);
		}
		
		try{
			stmt.execute(createIndexID);
		}catch(Exception ex){
			stmt.execute("alter table idList drop index idListIndex");
			stmt.execute(createIndexID);
		}
	    System.out.println("The index is created...");

	}

	void load_output_values(String directory, String[] file, String[] name,String[] header) throws Exception{
		for(int i=0;i<file.length;i++)
			load_output_values_specific(directory, file[i], name[i],header);
	}
	
	void load_output_values_specific(String directory, String file, String name,String[] header) throws Exception{
		System.out.println("Creating table for outcome "+name);
		Statement stmt=(Statement) con.createStatement();
		String createOutcomeTable="create table outcome_"+name+"(id varchar(50),outcome varchar(50))";
		String createOutcomeTempTable="create table outcomeTemp_"+name+"(id varchar(50),outcome varchar(50))";
		String createOutcomeIndex="create index outcome_"+name+"Index on outcome_"+name+"(id)";
		String createOutcomeRankTable="create table outcomeRank_"+name+"(id varchar(50),rank integer,var varchar(50),weight float)";
		String createOutcomeRankTempTable="create table outcomeRankTemp_"+name+"(id varchar(50),rank integer,var varchar(50),weight float)";
		String createOutcomeRankIndex="create index outcomeRank_"+name+"Index on outcomeRank_"+name+"(id,rank)";
		
		try{
			stmt.execute(createOutcomeTempTable);
		}catch(Exception ex){
			stmt.execute("drop table outcomeTemp_"+name);
			stmt.execute(createOutcomeTempTable);
		}
		
		try{
			stmt.execute(createOutcomeRankTempTable);
		}catch(Exception ex){
			stmt.execute("drop table outcomeRankTemp_"+name);
			stmt.execute(createOutcomeRankTempTable);
		}
		
		try{
			stmt.execute(createOutcomeTable);
		}catch(Exception ex){
			stmt.execute("drop table outcome_"+name);
			stmt.execute(createOutcomeTable);
		}
		
		try{
			stmt.execute(createOutcomeRankTable);
		}catch(Exception ex){
			stmt.execute("drop table outcomeRank_"+name);
			stmt.execute(createOutcomeRankTable);
		}
		System.out.println("Table created for outcome "+name);
		
		System.out.println("Reading outcome for "+name);
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    br.readLine();
	    
	    int i=0;
	    StringBuilder sqlValues=new StringBuilder();
	    StringBuilder sqlRank=new StringBuilder();
	    while((line=br.readLine())!=null){
			if(i==0){
		    	sqlValues=new StringBuilder("insert into outcomeTemp_"+name+" values");
		    	sqlRank=new StringBuilder("insert into outcomeRankTemp_"+name+" values");
			}
		    	
    		String[] strArr=line.split(",");
    		sqlValues.append("(\""+strArr[0].trim()+"\",\""+Float.parseFloat(strArr[1].trim())*100+"\"),");
    		for(int j=1;j<header.length;j++)
    			sqlRank.append("(\""+strArr[0].trim()+"\","+j+",\""+header[Integer.parseInt(strArr[(j*2)+1])].trim()+"\","+strArr[j*2+2].trim()+"),");
    			
    		i++;
    		
    		if(i>250){
    			i=0;
    			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
    			stmt.execute(sqlRank.subSequence(0, sqlRank.length()-1).toString());
    		}    		
   		}
		if(i!=0){
			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
			stmt.execute(sqlRank.subSequence(0, sqlRank.length()-1).toString());
		}
		
	    br.close();
	  
	    stmt.execute("insert into outcome_"+name+" select map.accountNo, temp.outcome from idMap map,outcomeTemp_"+name+" temp where temp.id=map.id");
	    stmt.execute("drop table outcomeTemp_"+name);
	  
	    stmt.execute("insert into outcomeRank_"+name+" select map.accountNo, temp.rank, temp.var, temp.weight from idMap map,outcomeRankTemp_"+name+" temp where temp.id=map.id");
	    stmt.execute("drop table outcomeRankTemp_"+name);
	  
	    System.out.println("All Data for outcome "+name+" are read");
	    
	    System.out.println("Creating Index on the data for outcome "+name);
		try{
			stmt.execute(createOutcomeIndex);
		}catch(Exception ex){
			stmt.execute("alter table outcome_"+name+" drop index outcome_"+name+"Index");
			stmt.execute(createOutcomeIndex);
		}
		
		try{
			stmt.execute(createOutcomeRankIndex);
		}catch(Exception ex){
			stmt.execute("alter table outcomeRank_"+name+" drop index outcomeRank_"+name+"Index");
			stmt.execute(createOutcomeRankIndex);
		}
	    System.out.println("The index is created...");


	}
	
	void load_idList(String directory, String file) throws Exception{
		
		System.out.println("Creating table for id list");
		Statement stmt=(Statement) con.createStatement();
		String createOutcomeTable="create table idList(id varchar(50),rifle integer,icu integer,mort integer,mv integer,cv integer,sepsis integer)";
		String createOutcomeDoneTable="create table idListDone(id varchar(50),rifle integer,icu integer,mort integer,mv integer,cv integer,sepsis integer)";
		String createOutcomeTempTable="create table idListTemp(id varchar(50),rifle integer,icu integer,mort integer,mv integer,cv integer,sepsis integer)";
		String createOutcomeIndex="create index idListIndex on idList(id)";
		
		try{
			stmt.execute(createOutcomeTempTable);
		}catch(Exception ex){
			stmt.execute("drop table idListTemp");
			stmt.execute(createOutcomeTempTable);
		}
		
		try{
			stmt.execute(createOutcomeTable);
		}catch(Exception ex){
			stmt.execute("drop table idList");
			stmt.execute(createOutcomeTable);
		}
		
		try{
			stmt.execute(createOutcomeDoneTable);
		}catch(Exception ex){
			stmt.execute("drop table idListDone");
			stmt.execute(createOutcomeDoneTable);
		}
		
		
		System.out.println("Reading idList");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    br.readLine();
	    
	    int i=0;
	    StringBuilder sqlValues=new StringBuilder();
	    while((line=br.readLine())!=null){
			if(i==0){
		    	sqlValues=new StringBuilder("insert into idListTemp values");
			}
		    	
    		String[] strArr=line.split(",");
    		sqlValues.append("(\""+strArr[0].trim()+"\","+Integer.parseInt(strArr[1].trim())+","+Integer.parseInt(strArr[2].trim())+","+Integer.parseInt(strArr[3].trim())+","+Integer.parseInt(strArr[4].trim())+","+Integer.parseInt(strArr[5].trim())+","+Integer.parseInt(strArr[6].trim())+"),");
    			
    		i++;
    		
    		if(i>250){
    			i=0;
    			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
    		}    		
   		}
		if(i!=0){
			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		}
		
	    br.close();
	  
	    stmt.execute("insert into idList select map.accountNo, temp.rifle, temp.icu, temp.mort, temp.mv, temp.cv, temp.sepsis from idMap map,idListTemp temp where temp.id=map.id");
	    stmt.execute("drop table idListTemp");
	 
	    System.out.println("All Data for id List are read");
	    
	    System.out.println("Creating Index on the data for idList ");
	    
		try{
			stmt.execute(createOutcomeIndex);
		}catch(Exception ex){
			stmt.execute("alter table idList drop index idListIndex");
			stmt.execute(createOutcomeIndex);
		}
	    System.out.println("The index is created...");

	}
}
