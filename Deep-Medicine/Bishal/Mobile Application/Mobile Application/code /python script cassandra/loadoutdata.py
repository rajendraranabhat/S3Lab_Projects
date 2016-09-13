#!/usr/bin/python
# -*- coding: utf-8 -*-

from cassandra.cluster import Cluster
import logging
import time

log = logging.getLogger()
log.setLevel('INFO')

class SimpleClient:
    session = None
    # log.info(userInfo)
    # userInfo2 =
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
        # self.session.execute(
        #     """CREATE KEYSPACE simplex WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};""")
        # self.session.execute("""
        #        CREATE TABLE prisma.songs (
        #            id uuid PRIMARY KEY,
        #            title text,
        #            album text,
        #            artist text,
        #            tags set<text>,
        #            data blob
        #        );
        #    """)
        # self.session.execute("""
        #        CREATE TABLE simplex.playlists (
        #            id uuid,
        #            title text,
        #            album text,
        #            artist text,
        #            song_id uuid,
        #            PRIMARY KEY (id, title, album, artist)
        #        );
        #    """)
        self.session.execute("""

    CREATE TABLE prisma.userInfo(
                Id timeuuid,
                userId varchar ,
                password varchar,
                gender varchar,
                age varchar,
                role varchar,
                speciality varchar,
                experience varchar,
                PRIMARY KEY(Id , userId)
                );

        """ )

        log.info('table userInfo created.')

        self.session.execute ("""
    CREATE TABLE  prisma.doctorTestResults(
                Id timeuuid,
                userId varchar ,
                quesNo  int,
                ansDoc varchar,
                PRIMARY KEY (Id,userId , quesNo)
                );
    """)
        log.info('table doctorTestResults created.')

        self.session.execute("""
    CREATE TABLE prisma.indexPatient(
                Id timeuuid,
                userID varchar,
                patientID varchar,
                attempt int,
                timeScreen1 float,
                PRIMARY KEY(Id)
                );

        """)
        log.info('table indexpatient created.')

        self.session.execute("""
    CREATE TABLE prisma.outcomeRank(
                Id timeuuid,
                userId varchar,
                patientID varchar,
                outcomeID int,
                feature varchar,
                PRIMARY KEY(Id)
            );
        """)
        log.info('table outcomeRank created')

        self.session.execute("""
    CREATE TABLE prisma.outcomeResult(
                Id timeuuid,
                userId varchar,
                patientID varchar,
                outcomeID int,
                attempt1 int,
                attempt2 int,
                PRIMARY KEY(Id, userID, patientID)
            );

        """)
        log.info('table outcomeResult created')

        self.session.execute("""
            CREATE TABLE prisma.outcomeStats(
                        Id timeuuid,
                        userId varchar,
                        patientID varchar,
                        outcomeID int,
                        timeScreen1 float,
                        timeScreen2 float,
                        click1 int,
                        click2 int,
                        PRIMARY KEY(Id, userID, patientID)
                    );

                """)
        log.info('table outcomeResult created')

        self.session.execute("""
            CREATE TABLE prisma.recoTakenTable(
                        Id timeuuid,
                        userId varchar,
                        patientID varchar,
                        reco varchar,
                        PRIMARY KEY(Id, userID, patientID)
                    );

                """)
        log.info('table recoTakenTable created')

        self.session.execute("""
                CREATE TABLE prisma.recoCaseTable(
                            Id timeuuid,
                            userId varchar,
                            patientID varchar,
                            caseNo varchar,
                            PRIMARY KEY(Id, userID, patientID)
                        );

                    """)
        log.info('table recoCaseTable created')

        self.session.execute("""
                CREATE TABLE prisma.recoTable(
                            Id timeuuid,
                            userId varchar,
                            patientID varchar,
                            reco varchar,
                            PRIMARY KEY(Id, userID, patientID)
                        );

                    """)
        log.info('table recoTable created')

    def delete_schema(self):

        self.session.execute("""
        DROP TABLE prisma.userInfo;
        """)
        self.session.execute("""
        DROP TABLE prisma.doctorTestResults;
         """)
        self.session.execute("""
         DROP TABLE prisma.indexPatient;
                 """)
        self.session.execute("""
         DROP TABLE prisma.outcomeRank;
                         """)
        self.session.execute("""
        DROP TABLE prisma.outcomeResult;
                         """)
        self.session.execute("""
        DROP TABLE prisma.outcomeStats;
                        """)
        self.session.execute("""
        DROP TABLE prisma.recoTakenTable;
                                """)
        self.session.execute("""
        DROP TABLE prisma.recoCaseTable;
                                """)
        self.session.execute("""
        DROP TABLE prisma.recoTable;

                              """)







        # """)

    def load_data(self):
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