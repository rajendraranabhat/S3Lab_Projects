import java.sql.DriverManager;
import java.sql.SQLException;
import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;

public class LoadOutputData {
	
static Connection con=null;
	
	public static void main(String[] args) throws Exception {
		LoadOutputData lod=new LoadOutputData();
		createConnection();
		lod.create();
		con.close();
	}
	
	static void createConnection() throws ClassNotFoundException, SQLException{
		Class.forName("com.mysql.jdbc.Driver");
		con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "panda", "shands@UF");
		
	}
	
	void create() throws Exception{
		
		Statement stmt=(Statement) con.createStatement();
		//String userInfo="create table userInfo(id varchar(50), password varchar(50), gender varchar(50), age varchar(50), role varchar(50), speciality varchar(50), experience varchar(50))";
		String doctorTestResults="create table doctorTestResults(id varchar(50), quesNo integer, ansDoc varchar(25))";
		String indexPatient="create table indexPatient(user varchar(50), id varchar(50), attempt integer, timeScreen1 float)";
		String outcomeRank="create table outcomeRank(user varchar(50),id varchar(50), outcomeID integer,feature varchar(50))";
		String outcomeResult="create table outcomeResult(user varchar(50),id varchar(50), outcomeID integer, attempt1 integer, attempt2 integer)";
		String outcomeStats="create table outcomeStats(user varchar(50),id varchar(50), outcomeID integer, timeScreen1 float, timeScreen2 float,click1 integer, click2 integer)";
		String recoTakenTable="create table recoTakenTable(id varchar(50),user varchar(50),reco varchar(5))";
		String recoCaseTable="create table recoCaseTable(id varchar(50),user varchar(50),caseno varchar(50))";
		String recoTable="create table recoTable(id varchar(50),user varchar(50),reco varchar(5))";
		
		/*try{
			stmt.execute(userInfo);
		}catch(Exception ex){
			stmt.execute("drop table userInfo");
			stmt.execute(userInfo);
		}*/
		
		try{
			stmt.execute(doctorTestResults);
		}catch(Exception ex){
			stmt.execute("drop table doctorTestResults");
			stmt.execute(doctorTestResults);
		}
		
		try{
			stmt.execute(indexPatient);
		}catch(Exception ex){
			stmt.execute("drop table indexPatient");
			stmt.execute(indexPatient);
		}
		
		try{
			stmt.execute(outcomeRank);
		}catch(Exception ex){
			stmt.execute("drop table outcomeRank");
			stmt.execute(outcomeRank);
		}
		
		try{
			stmt.execute(outcomeResult);
		}catch(Exception ex){
			stmt.execute("drop table outcomeResult");
			stmt.execute(outcomeResult);
		}
		
		try{
			stmt.execute(outcomeStats);
		}catch(Exception ex){
			stmt.execute("drop table outcomeStats");
			stmt.execute(outcomeStats);
		}
		
		try{
			stmt.execute(recoCaseTable);
		}catch(Exception ex){
			stmt.execute("drop table recoCaseTable");
			stmt.execute(recoCaseTable);
		}
		
		try{
			stmt.execute(recoTakenTable);
		}catch(Exception ex){
			stmt.execute("drop table recoTakenTable");
			stmt.execute(recoTakenTable);
		}
		
		try{
			stmt.execute(recoTable);
		}catch(Exception ex){
			stmt.execute("drop table recoTable");
			stmt.execute(recoTable);
		}
	}

}
	
