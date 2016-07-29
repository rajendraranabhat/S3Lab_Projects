package com.prisma.restapi;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Host;
import com.datastax.driver.core.Metadata;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;
import com.datastax.driver.core.Statement;
import com.datastax.driver.core.policies.DefaultRetryPolicy;
import com.datastax.driver.core.querybuilder.QueryBuilder;

public class CassandraDemo {
	
	private Cluster cluster;
	private Session session;
	
	public void connect(String node, int port) {
		cluster = Cluster.builder().addContactPoint(node)
								   .withRetryPolicy(DefaultRetryPolicy.INSTANCE)
								   //.withLoadBalancingPolicy(new TokenAwarePolicy(new DCAwareRoundRobinPolicy()))
                         			.build();
		                 			//.addContactPoint(node).withPort(port).build();
		Metadata metadata = cluster.getMetadata();
		System.out.printf("Cluster: %s\n", metadata.getClusterName());
		for ( Host host : metadata.getAllHosts() ) {
			System.out.printf("Host: %s \n",host.getAddress());
		}
		session = cluster.connect();
	}
	
	public void close(){
		cluster.close();
	}
	
	public void createSchema(){
		session.execute("CREATE KEYSPACE IF NOT EXISTS portfolio_demo " +
		"WITH REPLICATION = { 'class': 'SimpleStrategy', " +
		"'replication_factor': 1 };");
		
		session.execute("CREATE TABLE IF NOT EXISTS portfolio_demo.portfolio (" +
		"portfolio_id UUID, ticker TEXT, " +
		"current_price DECIMAL, current_change DECIMAL, " +
		"current_change_percent FLOAT, " +
		"PRIMARY KEY(portfolio_id, ticker));");
	}
	
	public void loadData(){
		session.execute("INSERT INTO portfolio_demo.portfolio " +
		"(portfolio_id, ticker, current_price, " +
		" current_change, current_change_percent) VALUES " +
		"(756716f7-2e54-4715-9f00-91dcbea6cf50, 'GOOG', " +
		" 889.07, -4.00, -0.45);");
		
		session.execute("INSERT INTO portfolio_demo.portfolio " +
		"(portfolio_id, ticker, current_price, " +
		" current_change, current_change_percent) VALUES " +
		"(756716f7-2e54-4715-9f00-91dcbea6cf50, 'AMZN', " +
		" 297.92, -0.94, -0.31);");
	}
	
	public void printResults(){
	ResultSet results = session.execute("SELECT * FROM " +
	"portfolio_demo.portfolio WHERE portfolio_id = " +
	"756716f7-2e54-4715-9f00-91dcbea6cf50;");
	
		for (Row row : results) {
			System.out.println(String.format("%-7s\t%-7s\t%-7s\t%-7s \n%s",
					"Ticker", "Price", "Change", "PCT",
					"........+........+........+........"));
		
			/*System.out.println(String.format("%-7s\t%0.2f\t%0.2f\t%0.2f",row.getString("ticker"),			
					row.getDecimal("current_price"),
					row.getDecimal("current_change"),
					row.getFloat("current_change_percent") ));*/
		System.out.println(row.getString("ticker")+" "+row.getDecimal("current_price")+" "+
					row.getDecimal("current_change")+" "+row.getFloat("current_change_percent"));
		}
	}
	
	public void testCqlsh(){
		// Insert one record into the users table
		//session.execute("INSERT INTO portfolio_demo.users (lastname, age, city, email, firstname) VALUES ('Jones', 35, 'Austin', 'bob@example.com', 'Bob')");
		// Use select to get the user we just entered
		ResultSet results = session.execute("SELECT * FROM portfolio_demo.users WHERE lastname='Jones'");
		
		for (Row row : results) {
			System.out.format("%s %d\n", row.getString("firstname"), row.getInt("age"));
		}
		
		// Update the same user with a new age
		//session.execute("update portfolio_demo.users set age = 36 where lastname = 'Jones'");
		// Select and show the change
		/*results = session.execute("select * from portfolio_demo.users where lastname='Jones'");
		for (Row row : results) {
			System.out.format("%s %d\n", row.getString("firstname"), row.getInt("age"));
		}*/
		
		// Delete the user from the users table
		//session.execute("DELETE FROM portfolio_demo.users WHERE lastname = 'Jones'");
		// Show that the user is gone
		/*results = session.execute("SELECT * FROM portfolio_demo.users");
		for (Row row : results) {
			System.out.format("%s %d %s %s %s\n", row.getString("lastname"), row.getInt("age"),  row.getString("city"), row.getString("email"), row.getString("firstname"));
		}	*/
		
		/*PreparedStatement statement = session.prepare("INSERT INTO portfolio_demo.users" + "(lastname, age, city, email, firstname)"
													   + "VALUES (?,?,?,?,?);");
		BoundStatement boundStatement = new BoundStatement(statement);
		session.execute(boundStatement.bind("Jones", 35, "Austin", "bob@example.com", "Bob"));*/
		
		// Use select to get the user we just entered
		/*Statement select = QueryBuilder.select().all().from("portfolio_demo", "users")
						.where(QueryBuilder.eq("lastname", "Jones"));
		results = session.execute(select);
		for (Row row : results) {
				System.out.format("%s %d \n", row.getString("firstname"),row.getInt("age"));
		}*/
		
		// Update the same user with a new age
		/*Statement update = QueryBuilder.update("portfolio_demo", "users")
										.with(QueryBuilder.set("age", 36))
										.where((QueryBuilder.eq("lastname", "Jones")));
		session.execute(update);
		// Select and show the change
		Statement select = QueryBuilder.select().all().from("portfolio_demo", "users")
									  .where(QueryBuilder.eq("lastname", "Jones"));
		results = session.execute(select);
		for (Row row : results) {
				System.out.format("%s %d \n", row.getString("firstname"),row.getInt("age"));
		}*/
		
		// Delete the user from the users table
        //Statement delete = QueryBuilder.delete().from("portfolio_demo.users")
		//							   .where(QueryBuilder.eq("lastname", "Jones"));
		
		/*results = session.execute(delete);
		// Show that the user is gone
		Statement select = QueryBuilder.select().all().from("portfolio_demo", "users");
		results = session.execute(select);
		for (Row row : results) {
			System.out.format("%s %d %s %s %s\n", row.getString("lastname"),
									row.getInt("age"), row.getString("city"),
									row.getString("email"), row.getString("firstname"));
		}*/
		
	}
		
	public static void main(String[] args) {
		CassandraDemo client = new CassandraDemo();
		client.connect("deepc04.acis.ufl.edu",9042);
		//client.createSchema();
		//client.loadData();
		//client.printResults();
		client.testCqlsh();
		client.close();
	}
}


