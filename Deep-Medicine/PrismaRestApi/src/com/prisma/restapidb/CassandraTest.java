package com.prisma.restapidb;

import java.util.ArrayList;

import com.datastax.driver.core.Session;
import com.google.gson.Gson;

public class CassandraTest {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		String feeds = null;
		try {
			ArrayList<FeedObjects> feedData = null;
			ProjectManager projectManager = new ProjectManager();
			feedData = projectManager.GetFeeds();
			Gson gson = new Gson();
			System.out.println(gson.toJson(feedData));

		} catch (Exception e) {
			System.out.println("error");
		}
	}
}
