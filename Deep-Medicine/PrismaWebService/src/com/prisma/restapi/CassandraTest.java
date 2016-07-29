package com.prisma.restapi;

import java.util.ArrayList;

import com.datastax.driver.core.Session;
import com.google.gson.Gson;

public class CassandraTest {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		String feeds = null;
		try {
			ArrayList<ScorePojo> feedData = null;
			PrismaManager projectManager = new PrismaManager();
			feedData = projectManager.GetScoreObj();
			Gson gson = new Gson();
			System.out.println(gson.toJson(feedData));

		} catch (Exception e) {
			System.out.println("error");
		}
	}
}
