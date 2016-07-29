#! /bin/bash
# file: prep.sh			G. Moody		13 February 2011
#	revised			I. Silva		 7 April    2011
# Create PostgreSQL account and database directory for MIMIC Importer

# Log in as the user who will own the MIMIC2 database, then run this script
# as root (either by "sudo ./prep.sh" or by "su root ./prep.sh").

# Check that PostgreSQL is installed.
if ( which psql 2>&1 | grep which >/dev/null )
then
    echo "PostgreSQL does not appear to be installed.  See Appendix A of the"
    echo "README for installation instructions."
    exit
fi

# Check that the PostgreSQL server is running.
if ( psql 2>&1 | grep "connect" >/dev/null )
then
    echo "The PostgreSQL server does not appear to be running.  See Appendix A"
    echo "of the README for instructions."
    exit
fi

# Check that we have root permissions first.
if [ $UID != 0 ]
then
    echo "This script must be run with superuser permissions, either by"
    echo "   sudo $0"
    echo "      or by"
    echo "   su root $0"
    exit
fi

# Get the login name of the user (not root)
if [ "x$SUDO_USER" == "x" ]
then
    U=$USER
else
    U=$SUDO_USER
fi
while [ "x$U" == "x" ]
do
    echo -n "Enter the login name of the database owner: "
    read U
done
if [ "$U" == "root" ]
then
    echo "The database cannot be owned by 'root'"
    exit
fi
if ! id $U >/dev/null 2>&1
then
    echo "No user named '$U' exists, cancelling."
    exit
fi

# Create a "role" (PostgreSQL account) with the same name as the user's
# login name on this system.  This allows PostgreSQL to use the login
# credentials to authenticate the user's identity.
#
# Before creating the role, check if it exists already.  If so, don't
# attempt to create it.  (Note: in this case, the role must already have
# create-database and postgres-superuser privileges, or we will have problems
# later!)

echo "psql postgres -c \"select * from pg_user where usename='$U';\"" >chrole.sh
chmod +x chrole.sh
if su postgres ./chrole.sh | grep $U >/dev/null
then
    echo "A PostgreSQL role named '$U' exists already;  reusing it."
else
    echo Creating PostgreSQL role "$U" ...
    echo createuser -d -R -s $U >crole.sh
    chmod +x crole.sh
    su postgres ./crole.sh
fi
rm -f chrole.sh crole.sh

# Make a directory for storage of MIMIC2
su postgres ./data-directory-name.sh >ddname
DBDIR=`cat ddname`/mimic2v26_dat
rm -f ddname
if [ -d $DBDIR ]
then
    echo "$DBDIR exists already;  reusing it."
else
    echo Creating $DBDIR for PostgreSQL tablespace.
    mkdir -p $DBDIR
    chown postgres.postgres $DBDIR
fi



