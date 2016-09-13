import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.sql.DriverManager;
import java.sql.SQLException;
import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;

public class LoadMetadata {
	static Connection con=null;
	
	public static void main(String[] args) throws Exception {
		LoadMetadata lmd=new LoadMetadata();
		createConnection();
		String directory="/home/rbhat/Bishal/Web Application/Web Application/data";
		String pr1file="ICD9_pr1.csv";
		String mdcfile="MDC.csv";
		String medFile="medications.csv";
		String outcomefile="outcomes.csv";
		String varDefFile="variableDefinations.csv";
		String varValFile="variableMap.csv";
		
		//lmd.pr1_ip(directory, pr1file);
		//lmd.mdc_ip(directory, mdcfile);
		//lmd.med_ip(directory, medFile);
		//lmd.outcome_ip(directory, outcomefile);
		//lmd.variableDefination_ip(directory, varDefFile);
		lmd.variableMap_ip(directory, varValFile);
		
		con.close();
	}
	
	
	static void createConnection() throws ClassNotFoundException, SQLException{
		Class.forName("com.mysql.jdbc.Driver");
		//con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "panda", "shands@UF");
		con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "root", "");
		
	}
	
	void pr1_ip(String directory, String file) throws Exception{
		System.out.println("Creating table to enter ICD9 details...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table pr1Map(id varchar(10), description varchar(300))";
		String createIndex="create index pr1MapIndex on pr1Map(id)";
		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table pr1Map");
			stmt.execute(createTable);
		}
		System.out.println("Table created to enter pr1 details...");
		
		System.out.println("Reading pr1 Map file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    
	    StringBuilder sqlValues=new StringBuilder();
	    int i=0;
	    while((line=br.readLine())!=null){
			if(i==0)
		    	sqlValues=new StringBuilder("insert into pr1Map values");
		    	
    		String[] strArr=line.split(";");
    		//System.out.println(line);
    		sqlValues.append("(\""+strArr[0].trim()+"\",\""+strArr[1].trim()+"\"),");
    		
    		i++;
    		
    		if(i>500){
    			i=0;
    			//System.out.println(sqlValues.subSequence(0, sqlValues.length()-1).toString());
    			//System.exit(0);
    			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
    		}    		
   		}
		if(i!=0)
			stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    System.out.println("All Data of pr1 details are entered...");
	    
	    System.out.println("Creating Index on the data of pr1 details");
		try{
			stmt.execute(createIndex);
		}catch(Exception ex){
			stmt.execute("alter table icd9Map drop index pr1MapIndex");
			stmt.execute(createIndex);
		}
	    System.out.println("The index is created...");
	}

	void mdc_ip(String directory, String file) throws Exception{
		System.out.println("Creating table to enter ICD9 details...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table mdcMap(id varchar(10), description varchar(200))";
		
		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table mdcMap");
			stmt.execute(createTable);
		}
		System.out.println("Table created to enter mdc details...");
		
		System.out.println("Reading mdc Map file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    
	    StringBuilder sqlValues=new StringBuilder();
	    int i=0;
	    while((line=br.readLine())!=null){
			if(i==0)
		    	sqlValues=new StringBuilder("insert into mdcMap values");
		    	
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
	    System.out.println("All Data of mdc details are entered...");
	    
	}
	
	void outcome_ip(String directory, String file) throws Exception{
		System.out.println("Creating table to enter the outcomes...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table outcomes(id integer,outcome varchar(20), description varchar(110))";

		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table outcomes");
			stmt.execute(createTable);
		}
		System.out.println("Table created to enter the outcomes...");
		
		System.out.println("Reading the outcomes file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	   
	    
	    StringBuilder sqlValues=new StringBuilder();
	    sqlValues=new StringBuilder("insert into outcomes values");
	    while((line=br.readLine())!=null){
    		String[] strArr=line.split(";");
    		sqlValues.append("("+Integer.parseInt(strArr[0].trim())+",\""+strArr[1].trim()+"\",\""+strArr[2].trim()+"\"),");    		
   		}

	    stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    System.out.println("All Data of the outcomes are entered...");
	}
	
	void med_ip(String directory, String file) throws Exception{
		System.out.println("Creating table to enter the outcomes...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table medicine(id varchar(20), description varchar(20))";

		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table medicine");
			stmt.execute(createTable);
		}
		System.out.println("Table created to enter the medicines...");
		
		System.out.println("Reading the medicines file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	   
	    
	    StringBuilder sqlValues=new StringBuilder();
	    sqlValues=new StringBuilder("insert into medicine values");
	    while((line=br.readLine())!=null){
    		String[] strArr=line.split(",");
    		sqlValues.append("(\""+strArr[0].trim()+"\",\""+strArr[1].trim()+"\"),"); 
   		}

	    stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    System.out.println("All Data of the medicines are entered...");
	}

	void variableDefination_ip(String directory, String file) throws Exception{
		System.out.println("Creating table to enter variable defination details...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table varDef(id varchar(20), type varchar(20) ,description varchar(100))";
		String createIndex="create index varDefIndex on varDef(id)";
		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table varDef");
			stmt.execute(createTable);
		}
		System.out.println("Table created to enter variable defination details...");
		
		System.out.println("Reading variable defination file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    
	    StringBuilder sqlValues=new StringBuilder("insert into varDef values");
	
	    while((line=br.readLine())!=null){	
    		String[] strArr=line.split(";");
    		sqlValues.append("(\""+strArr[1].trim()+"\",\""+strArr[0].trim()+"\",\""+strArr[2].trim()+"\"),");    		
   		}
		
		stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    System.out.println("All Data of variable defination details are entered...");
	    
	    System.out.println("Creating Index on the data of variable defination details");
		try{
			stmt.execute(createIndex);
		}catch(Exception ex){
			stmt.execute("alter table varDef drop index varDefIndex");
			stmt.execute(createIndex);
		}
	    System.out.println("The index is created...");
	    
	    
	}
	
	void variableMap_ip(String directory, String file) throws Exception{
		System.out.println("Creating table to enter variable map details...");
		Statement stmt=(Statement) con.createStatement();
		String createTable="create table varMap(id varchar(20), map varchar(20) ,value varchar(50))";
		String createIndex="create index varMapIndex on varMap(id)";
		try{
			stmt.execute(createTable);
		}catch(Exception ex){
			stmt.execute("drop table varMap");
			stmt.execute(createTable);
		}
		System.out.println("Table created to enter variable map details...");
		
		System.out.println("Reading variable map file...");
		BufferedReader br= new BufferedReader(new FileReader(new File(directory+"//"+file)));
	    String line;
	    
	    StringBuilder sqlValues=new StringBuilder("insert into varMap values");
	    
	    while((line=br.readLine())!=null){
				
    		String[] strArr=line.split(",");
    		System.out.println(line);
    		String id=strArr[0];
    		String[] maps=strArr[1].trim().split(";");
    		for (String map : maps) {
    			String[] values=map.trim().split(":");
    			sqlValues.append("(\""+id+"\",\""+values[0].trim()+"\",\""+values[1].trim()+"\"),");
    			//System.out.println(sqlValues);
    			
			}
    		    		
   		}
	    
		//System.out.println(i);
		stmt.execute(sqlValues.subSequence(0, sqlValues.length()-1).toString());
		
	    br.close();
	    System.out.println("All Data of variable map details are entered...");
	    
	    System.out.println("Creating Index on the data of variable map details");
		try{
			stmt.execute(createIndex);
		}catch(Exception ex){
			stmt.execute("alter table varMap drop index varMapIndex");
			stmt.execute(createIndex);
		}
	    System.out.println("The index is created...");
	}
}

