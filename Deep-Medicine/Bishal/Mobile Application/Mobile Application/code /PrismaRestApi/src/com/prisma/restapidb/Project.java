package com.prisma.restapidb;

import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;
import com.datastax.driver.core.Statement;
import com.datastax.driver.core.policies.DefaultRetryPolicy;
import com.datastax.driver.core.querybuilder.QueryBuilder;

import java.sql.Connection;
import java.sql.PreparedStatement;
//import java.sql.ResultSet;
import java.util.ArrayList;

public class Project {

	public ArrayList<FeedObjects> GetFeeds(Session session)//(Connection connection)
			throws Exception {
		ArrayList<FeedObjects> feedData = new ArrayList<FeedObjects>();
		try {
			// String uname = request.getParameter("uname");
			ResultSet results = session.execute("SELECT title,description,url FROM prisma.website");
			
			for (Row row : results) {
				//System.out.format("%s %d\n", row.getString("firstname"), row.getInt("age"));
				FeedObjects feedObject = new FeedObjects();
				feedObject.setTitle(row.getString("title"));
				feedObject.setDescription(row.getString("description"));
				feedObject.setUrl(row.getString("url"));
				feedData.add(feedObject);
			}
			
			/*PreparedStatement ps = connection
					.prepareStatement("SELECT title,description,url FROM website ORDER BY id DESC");
			// ps.setString(1,uname);
			ResultSet rs = ps.executeQuery();
			while (rs.next()) {
				FeedObjects feedObject = new FeedObjects();
				feedObject.setTitle(rs.getString("title"));
				feedObject.setDescription(rs.getString("description"));
				feedObject.setUrl(rs.getString("url"));
				feedData.add(feedObject);
			}*/
			return feedData;
		} catch (Exception e) {
			throw e;
		}
	}
}


