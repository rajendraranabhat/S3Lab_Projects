#! /bin/sh
# file: resetdb.sh		G. Moody		13 February 2011
#
# Please think twice before running this program!!
#
# To reset the PostgreSQL database cluster to its initial state, run this
# script as root.  This was useful while debugging the MIMIC exporter,
# but it's dangerous to leave it around -- please remove it if you
# have no need for it.

echo "Warning: the entire PostgreSQL database cluster will be removed!"
echo -n "Are you sure you want to do this? [y/N]: "
read ANSWER
case $ANSWER in
  y*|Y*) echo "The database cluster will be removed in 5 seconds unless you interrupt this script."
	sleep 7
	service postgresql-9.0 stop
	rm -rf /var/lib/pgsql/9.0
	service postgresql-9.0 initdb
	service postgresql-9.0 start
	./prep.sh
	;;
     *) echo "Cancelled, no changes made."
	;;
esac
exit

