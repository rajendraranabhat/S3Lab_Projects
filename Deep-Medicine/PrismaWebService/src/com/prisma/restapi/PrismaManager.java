package com.prisma.restapi;

//import java.sql.Connection;
import com.datastax.driver.core.Session;
import java.util.ArrayList;

public class PrismaManager {

	public ArrayList<ScorePojo> GetScoreObj() throws Exception {
		ArrayList<ScorePojo> scoreLists = null;
		Dao dao = null;
		try {
			dao = new Dao();
			Session session = dao.getSession();
			Score project = new Score();
			scoreLists = project.GetScores(session);			
		} catch (Exception e) {
			throw e;
		}
		finally{
			if(dao !=null)
				dao.close();
		}
		
		return scoreLists;
	}
	
}
