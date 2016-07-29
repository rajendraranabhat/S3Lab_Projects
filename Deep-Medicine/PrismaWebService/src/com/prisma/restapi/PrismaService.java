package com.prisma.restapi;

import java.util.ArrayList;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import com.google.gson.Gson;

@Path("/WebService")
public class PrismaService {

	@GET
	@Path("/GetScores")
	@Produces("application/json")
	public String feed() {
		String feeds = null;
		try {
			ArrayList<ScorePojo> scoreLists = null;
			PrismaManager prismaManager = new PrismaManager();
			scoreLists = prismaManager.GetScoreObj();
			Gson gson = new Gson();
			System.out.println(gson.toJson(scoreLists));
			feeds = gson.toJson(scoreLists);

		} catch (Exception e) {			
			System.out.println("error");
		}
		return feeds;
	}
}
