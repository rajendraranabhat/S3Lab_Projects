import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;


public class SaveData {
	static Connection con=null;
	public static void main(String[] args) throws Exception {
		SaveData sd=new SaveData();
		createConnection();
		sd.saveUserInfo("userInfo");
		sd.saveUserInfo("doctorTestResults");
		sd.saveUserInfo("indexPatient");
		sd.saveUserInfo("outcomeRank");
		sd.saveUserInfo("outcomeResult");
		sd.saveUserInfo("outcomeStats");
		sd.saveUserInfo("recoTakenTable");
		sd.saveUserInfo("recoCaseTable");
		sd.saveUserInfo("recoTable");
		
		
		con.close();
	}
	
//	String userInfo="create table userInfo(id varchar(50), password varchar(50), gender varchar(50), age varchar(50), role varchar(50), speciality varchar(50), experience varchar(50))";
//	String doctorTestResults="create table doctorTestResults(id varchar(50), quesNo integer, ansDoc varchar(25))";
//	String indexPatient="create table indexPatient(user varchar(50), id varchar(50), attempt integer, timeScreen1 float)";
//	String outcomeRank="create table outcomeRank(id varchar(50), outcomeID integer,feature varchar(50))";
//	String outcomeResult="create table outcomeResult(id varchar(50), outcomeID integer, attempt1 integer, attempt2 integer)";
//	String outcomeStats="create table outcomeStats(id varchar(50), outcomeID integer, timeScreen1 float, timeScreen2 float,click1 integer, click2 integer)";
	
	
	static void createConnection() throws ClassNotFoundException, SQLException{
		Class.forName("com.mysql.jdbc.Driver");
		con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "panda", "shands@UF");
		
	}
	
	void saveUserInfo(String table) throws IOException, SQLException{
		SimpleDateFormat sdf=new SimpleDateFormat("MM_dd_hh_mm");
		Statement stmt=(Statement) con.createStatement();
		BufferedWriter bw=new BufferedWriter(new FileWriter(new File(table+"_"+sdf.format(new Date())+".csv")));
		
		ResultSet rs=stmt.executeQuery("select * from "+table);
		
		while(rs.next()){
			StringBuilder sb=new StringBuilder(rs.getString(1));
			for (int i = 2; i <= rs.getMetaData().getColumnCount(); i++) {
				sb.append(","+rs.getString(i));
			}
			bw.write(sb.toString());
			bw.newLine();
		}
		bw.close();
	}
}
