package com.prisma.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class ConnectHSQLDB {
	public static void main(String[] args) {
		Connection connection = null;
		ResultSet resultSet = null;
		Statement statement = null;
		try {
			Class.forName("org.hsqldb.jdbcDriver");
			connection = DriverManager.getConnection( 
			"jdbc:hsqldb:file:/home/rbhat/workspace/S3Lab_Projects/Deep-Medicine/HSQLDB_PRISMA", "SA", "");
			statement = connection.createStatement();
			resultSet = statement
					.executeQuery("SELECT Salary FROM SALARYDETAILS WHERE Emptitle='54601A'");
			while (resultSet.next()) {
				System.out.println("EMPLOYEE Salary:"
						+ resultSet.getString("Salary"));
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				resultSet.close();
				statement.close();
				connection.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
}


