package com.prisma.restapidb;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Host;
import com.datastax.driver.core.Metadata;
import com.datastax.driver.core.Session;
import com.datastax.driver.core.policies.DefaultRetryPolicy;

public class Database {
	
	private Cluster cluster;
	private Session session = null;
	
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
		this.session = cluster.connect();
	}
	
	public void close(){
		this.session.close();
		this.cluster.close();
	}
	
	public Session getSession() throws Exception {
		try{
			if(this.session==null){
				connect("deepc04.acis.ufl.edu",9042);
			}				
		}
		catch(Exception e){
			throw e;
		}
		
		return this.session;
	}

	/*public Connection Get_Connection() throws Exception {
		try {
			String connectionURL = "jdbc:mysql://localhost:3306/workingbrain";
			Connection connection = null;
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			connection = DriverManager.getConnection(connectionURL, "root", "");
			return connection;
		} catch (SQLException e) {
			throw e;
		} catch (Exception e) {
			throw e;
		}
	}*/

}
