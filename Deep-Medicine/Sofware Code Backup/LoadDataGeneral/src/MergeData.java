import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;


public class MergeData {
	static Connection con=null;
	public static void main(String[] args) throws Exception {
		MergeData sd=new MergeData();
		createConnection();
		//sd.saveUserInfo("userInfo","select id, password, gender, age, role, speciality, experience from userInfo");
		//sd.saveUserInfo("doctorTestResults","select id, quesNo, ansDoc from doctorTestResults");
		//sd.saveUserInfo("indexPatient","select user, id, attempt, timeScreen1 from indexPatient");
		sd.saveUserInfo("OutcomeRank","select id, outcomeID,feature from outcomeRank");
		//sd.saveUserInfo("outcomeResult","select id, outcomeID, attempt1, attempt2,user,oname from outcomeResult,outcome where outcomeID=oid order by user");
		//sd.saveUserInfo("outcomeStats","select id, outcomeID, timeScreen1, timeScreen2,click1, click2,user,oname from outcomeStats,outcome where outcomeID=oid order by user");
		con.close();
	}
	
	
	static void createConnection() throws ClassNotFoundException, SQLException{
		Class.forName("com.mysql.jdbc.Driver");
		con=(Connection) DriverManager.getConnection("jdbc:mysql://localhost:3306/medical", "panda", "shands@UF");
		
	}
	
	void saveUserInfo(String table, String SQL) throws IOException, SQLException{
		Statement stmt=(Statement) con.createStatement();
		BufferedWriter bw=new BufferedWriter(new FileWriter(new File("C:\\Users\\spuri\\Desktop\\Data\\"+table+".csv"),true));
		
		ResultSet rs=stmt.executeQuery(SQL);
		
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
