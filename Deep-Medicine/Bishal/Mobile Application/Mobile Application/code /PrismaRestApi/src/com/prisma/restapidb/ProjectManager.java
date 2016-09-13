package com.prisma.restapidb;

//import java.sql.Connection;
import com.datastax.driver.core.Session;
import java.util.ArrayList;

public class ProjectManager {

	public ArrayList<FeedObjects> GetFeeds() throws Exception {
		ArrayList<FeedObjects> feeds = null;
		Database database = null;
		try {
			database = new Database();
			Session session = database.getSession();
			//Connection connection = database.Get_Connection();
			Project project = new Project();
			//feeds = project.GetFeeds(connection);
			feeds = project.GetFeeds(session);

		} catch (Exception e) {
			throw e;
		}
		finally{
			if(database !=null)
				database.close();
		}
		
		return feeds;
	}
	
}
