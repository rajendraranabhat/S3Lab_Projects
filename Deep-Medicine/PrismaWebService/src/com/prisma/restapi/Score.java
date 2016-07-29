package com.prisma.restapi;

import java.util.ArrayList;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;

public class Score {

	public ArrayList<ScorePojo> GetScores(Session session)//(Connection connection)
			throws Exception {
		ArrayList<ScorePojo> scoreList = new ArrayList<ScorePojo>();
		try {
			// String uname = request.getParameter("uname");
			ResultSet results = session.execute("select accountno, cat_30d, cat_cv, cat_icu, cat_mv, pred_30d, pred_cv, pred_icu, pred_mv from prisma.score");
			
			for (Row row : results) {
				//System.out.format("%s %d\n", row.getString("firstname"), row.getInt("age"));
				ScorePojo score = new ScorePojo();
				score.setAccountno(row.getString("accountno"));
				score.setCat_30d(row.getString("cat_30d"));
				score.setCat_cv(row.getString("cat_cv"));
				score.setCat_icu(row.getString("cat_icu"));
				score.setCat_mv(row.getString("cat_mv"));
				score.setPred_30d(row.getDouble("pred_30d"));
				score.setPred_cv(row.getDouble("pred_cv"));
				score.setPred_icu(row.getDouble("pred_icu"));
				score.setPred_mv(row.getDouble("pred_mv"));
				scoreList.add(score);
			}
			
			return scoreList;
		} catch (Exception e) {
			throw e;
		}
	}
}


