package com.prisma.restapi;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Host;
import com.datastax.driver.core.Metadata;
import com.datastax.driver.core.Session;
import com.datastax.driver.core.policies.DefaultRetryPolicy;

public class Dao {
	
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

}
