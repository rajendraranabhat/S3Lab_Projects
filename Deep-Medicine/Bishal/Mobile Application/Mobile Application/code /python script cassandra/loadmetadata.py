#!/usr/bin/python
# -*- coding: utf-8 -*-

from cassandra.cluster import Cluster
import logging
import time
from array import array

log = logging.getLogger()
log.setLevel('INFO')

class SimpleClient:
    session = None

    def connect(self, nodes):
        cluster = Cluster(nodes)
        metadata = cluster.metadata
        self.session = cluster.connect()
        log.info('Connected to cluster: ' + metadata.cluster_name)
        #log.info(metadata)
        for host in metadata.all_hosts():
            log.info('Datacenter: %s; Host: %s; Rack: %s',
                host.datacenter, host.address, host.rack)

    def close(self):
        self.session.cluster.shutdown()
        self.session.shutdown()
        log.info('Connection closed.')

    def create_schema(self):

        self.session.execute("""

    CREATE TABLE prisma.pr1Map(

                timeId timeuuid,
                Id int ,
                description varchar

                );

        """ )

    log.info('table pr1Map created.')



    def delete_schema(self):

        self.session.execute("""
        DROP TABLE prisma.pr1Map;
        """)

    def load_data(self):

        #pr1 = open("/Users/bishalgautam/Downloads/ICD9_pr1.csv","rb")
        with open('/Users/bishalgautam/Downloads/ICD9_pr1.csv','rb') as fp:
            for line in fp:
               # print line
              strvalue = array(line.split(';'))
               

                # self.session.execute("""
        #        INSERT INTO simplex.songs (id, title, album, artist, tags)
        #        VALUES (
        #            756716f7-2e54-4715-9f00-91dcbea6cf50,
        #            'La Petite Tonkinoise',
        #            'Bye Bye Blackbird',
        #            'Joséphine Baker',
        #            {'jazz', '2013'}
        #        );
        #    """)
        # self.session.execute("""
        #        INSERT INTO prisma.users ( id, email, password)
        #        VALUES (
        #            now(),
        #            'sh@ufl.edu',
        #            'mittal'
        #
        #        );
        #    """)

         log.info('Data loaded.')


def main():
    logging.basicConfig()
    client = SimpleClient()
    client.connect(['128.227.246.38'])

    try:
        client.create_schema()
    except Exception:
        print "tables already exists"
        client.delete_schema()
        client.create_schema()
    # client.delete_schema()

    # time.sleep(10)
    # client.load_data()
    client.close()

if __name__ == "__main__":
    main()