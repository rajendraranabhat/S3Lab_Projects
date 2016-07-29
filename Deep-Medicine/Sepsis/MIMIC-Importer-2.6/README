file: README		George Moody and Ikaro Silva	13 February 2011
      			Last revised:	       		 5 December 2011
MIMIC Importer: Flat-file tools for the MIMIC II Clinical Database
____________________________________________________________________________

The MIMIC Importer is free software.  You can redistribute it and/or modify it
under the terms of the GNU General Public License version 2, as published by
the Free Software Foundation.

The MIMIC Importer is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
the MIMIC Importer.  If not, see <http://www.gnu.org/licenses/>.

You may contact the authors by e-mail (george@mit.edu or ikaro AT gmail DOT com)
or postal mail:

     MIT Room E25-505B
     77 Massachusetts Avenue
     Cambridge, MA 02139
     USA

For updates to this software, please visit PhysioNet:
     http://www.physionet.org
______________________________________________________________________________

This version of the MIMIC Importer imports the flat files for version 2.6 of
the MIMIC II Clinical Database into a PostgreSQL database.  It has been tested
using PostgreSQL versions 8.4.7 and 9.0.3 on Fedora 14 Linux, but it does not
rely on any advanced PostgreSQL or operating system features, and it should be
usable with any recent version of PostgreSQL on any platform.  It may also be
possible to adapt it for use with other relational database software. (We do
not recommend MySQL for this purpose, however, since it silently ignores check
constraints).

We recommend reading this entire document before beginning work.  If you are
an experienced PostgreSQL user, you will recognize that there are alternatives
to the steps outlined below (and if you have a suggestion for simplifying them,
please let us know).  Be warned that if you do the steps below out-of-order,
you may not obtain the desired results!

On a typical PC, the MIMIC Importer can load the entire MIMIC II Clinical
Database of about 33000 patients in a day or less, unattended.

The MIMIC Importer is under development, but it automates a large part of the
task of building a PostgreSQL database from the flat files, and it has been
made available in its present unfinished state for this reason.

I. Prerequisites
----------------

In addition to any recent version of the PostgreSQL server, you will need the
GNU 'bash' shell (command interpreter) and a variety of other common utilities
that are standard on all Unix-like platforms (including all versions of
FreeBSD, Linux, MacOS X, Solaris, and Unix, but not including Windows).  On
Windows, the necessary utilities are included in the free and open-source
Cygwin environment (http://www.cygwin.com), or you may be able to use
'import.sh' as a guide for writing your own script for Windows.  Note that
these utilities are only needed for loading the database with flat files using
the MIMIC Importer, and not for using the database.

As a rule of thumb, each set of about 1000 subjects adds about a gigabyte to
the size of the database.  You will need about 75 GB for storage of the entire
MIMIC II Clinical Database, and an additional 25 GB of workspace.

In the next section, steps 5 and 6 require root (superuser) privileges.
Your system administrator will be able to perform these steps, which will
require 5 minutes or less, if necessary.  Running the MIMIC Importer (step 7),
which can take up to a day if you are importing the entire database, does not
require root privileges.


II. Using the MIMIC Importer
-----------------------------

1. Log in as the user who will own the database, and open a terminal window
   (on Windows, a Cygwin window).  Type the commands required by the remaining
   steps in the terminal or Cygwin window.

2. Using your web browser, download and save MIMIC-Importer-2.6.tar.gz
   in a directory that contains at least 2 GB (and ideally 25 GB) of
   free space.

3. Returning to your terminal window, unpack the MIMIC Importer tarball:
      tar xfvz MIMIC-Importer-2.6.tar.gz
   If your browser has decompressed the MIMIC Importer tarball, its name will
   end with '.tar' rather than '.tar.gz'.  In this case, unpack it by:
      tar xfv MIMIC-Importer-2.6.tar
   This will create a 'MIMIC-Importer-2.6' directory containing shell scripts
   and a copy of this README file.

4. Using your web browser, download the tarballs (.tar.gz files) you will need,
   and save all of them in your 'MIMIC-Importer-2.6' directory.  You will need
   to download and save:
      mimic2cdb-2.6-Definitions.tar.gz
   as well as the tarballs containing subject-specific data:
      mimic2cdb-2.6-00.tar.gz
      mimic2cdb-2.6-01.tar.gz
   and so on.  It is not necessary to download all of the subject-specific data
   tarballs before continuing;  you can rerun the MIMIC Importer later on to
   load data for additional subjects if you wish.

5. If the PostgreSQL server is not already running on your system, follow the
   instructions in Appendix A to start it.  (If you're not sure, try step 6;
   it will tell you if you need to start the server.)  You will need root
   (superuser, administrator) privileges to do any of the steps in Appendix A.

6. To create a PostgreSQL "role" (user account) for yourself, and a location
   in the file system for storage of the database, type this command:
       sudo ./prep.sh
   Type your password when prompted.

   If this command fails, see Appendix B (Alternatives to 'sudo ./prep.sh')
   below.

7. Run the MIMIC Importer by typing
      ./import.sh
   to import all of the flat files you have downloaded.

   If you didn't download all of the flat files, you can get some or all
   of the rest later on, and run the MIMIC Importer again to load them.
   Note that the MIMIC Importer is optimized for efficiently loading
   records into a freshly-created database;  it will run much more slowly
   when adding records to an existing database.

See Appendix C for notes and troubleshooting hints for the MIMIC Importer.


Appendix A.  Starting the PostgreSQL server
--------------------------------------------

To use the MIMIC Importer, you need to have installed and started any recent
version of the PostgreSQL server.  We use and recommend PostgreSQL 8.4.7 and
9.0.3 on Fedora 14 GNU/Linux.  If you wish to replicate our setup, we've
provided step-by-step instructions below for installing and starting PostgreSQL
9.0.3 on Fedora 14.  You can find instructions for other versions of PostgreSQL
and other platforms at http://www.postgresql.org/docs/; details may vary, but
the sequence of steps should be quite similar.

1. Acquire root (superuser) privileges by logging in as "root", or by
   running "sudo -s" or "su".  Get help from your system administrator
   if necessary.  If the PostgreSQL server has already been installed,
   skip ahead to step 5 below.

2. In /etc/yum.repos.d/, edit fedora.repo, fedora-updates.repo, and (if you
   have it) fedora-updates-testing.repo, adding the line
     exclude-postgresql*
   at the end of each [fedora*] and [updates*] section.

3. Install the yum configuration and GPG key for PGDG RPMs:
     rpm -ivH http://yum.pgrpms.org/reporpms/9.0/pgdg-fedora-9.0-2.noarch.rpm

4. Install a basic PostgreSQL 9.0 server:
     yum install postgresql90-server
   This command pulls in other modules required by the server, including
   postgresql90 (the client) and postgresql90-libs (common shared libraries).
   There are many optional modules you can install at the same time or later,
   as you wish.  You won't need any of them to run the MIMIC Importer.

5. Initialize the database cluster in PGDATA (usually /var/lib/pgsql/9.0/data):
     service postgresql-9.0 initdb

6. (Optional) To start the server automatically after each reboot, run:
     chkconfig postgresql-9.0 on

7. To start the server without rebooting, run:
     service postgresql-9.0 start

If at some point you suspect your PostgreSQL installation is damaged, you can
start over from step 5 after running these commands as root:
    service postgresql stop
    rm -rf /var/lib/pgsql/9.0
or from step 4 after also running
    yum erase postgresql90-server postgresql90 postgresql90-libs
The 'rm' command will destroy any databases you have created using
PostgreSQL-9.0, so don't do this unless you have exhausted the alternatives.


Appendix B. Alternatives to 'sudo ./prep.sh'
--------------------------------------------

You will need to create a PostgreSQL "role" (user account) with the same name
as your system login name in order to run the MIMIC Importer.  You will also
need to create a mimic2v26_dat directory owned by 'postgres' for storage of
your MIMIC2 database.  'prep.sh' is a shell script (batch file) that does
this for you on most platforms, but there are other ways to accomplish the
same goals if 'prep.sh' doesn't work for you.

If you do not have root (superuser) privileges, get help from your system
administrator (or the person who installed PostgreSQL on your system), who does
have them.  On some platforms, superuser privileges are called 'administrator'
privileges.

Although running 'prep.sh' using 'sudo' works on most platforms, it can fail
for a variety of reasons, most often if 'sudo' is not set up on your system
or if you are not on the list of users who are allowed to use 'sudo'.  In
this case, either configure 'sudo' so that you can use it, or run 'prep.sh'
using 'su', like this:
    su root prep.sh
and type the root password when prompted.

Another possibility on some platforms is to login as root, navigate to this
directory, and run
    ./prep.sh

Another reason that 'prep.sh' may fail is if the current directory is not
writable by root (either because it is on a read-only file system or, more
likely, an NFS or other network-mounted file system for which root is denied
write privileges).  In this case, copy 'prep.sh' to a root-writable file
system and try running it there.  ('prep.sh' needs to write three very short
temporary files in the current directory.)

If you cannot use 'prep.sh' even after trying the alternative ways of running
it outlined above, follow these steps instead:

1. Acquire root (superuser) privileges.

2. Create a directory for the database, within a directory owned by user
   'postgres':
       mkdir /var/lib/pgsql/9.0/data/mimic2v26_dat
   Do not reuse an existing directory for this purpose.  At least 75 GB should
   be available for the fully loaded database.

   In the example, /var/lib/pgsql/9.0/data/ is the location of the default data
   directory (see step 5, Appendix A) on Fedora 14; this location may vary on
   other platforms.

3. Make 'postgres' the owner of the database directory:
       chown postgres.postgres /var/lib/pgsql/9.0/data/mimic2v26_dat

4. Acquire postgres privileges.  On most platforms, do this by running
       su - postgres
   (note the spaces before and after the hyphen).

5. Create a "role" (PostgreSQL user account) for the database owner, if you
   have not already done so, by running:
       createuser -d -R -s username
   (replacing "username" with the database owner's system login account name).

It's important to use an existing login account name before creating the
PostgreSQL role, because doing so allows the PostgreSQL server to use the system
login credentials for access control.


Appendix C. Notes and troubleshooting hints
-------------------------------------------

Here's what happens when you run the MIMIC Importer (import.sh):
 * It unpacks the definitions from mimic2cdb-2.6-Definitions.tar.gz (or
   mimic2cdb-2.6-Definitions.tar, if your browser has decompressed it).
 * If the MIMIC2 database exists already:
    - The MIMIC Importer asks you to confirm that you wish to load more data.
      If not, you can cancel and leave your existing MIMIC2 database unaltered.
 * Otherwise:
    - The MIMIC Importer looks for a 'mimic2v26_dat' directory in the default
      location (Appendix A, step 5);  if it's not there, the Importer asks you
      where to find it.
    - The MIMIC Importer creates MIMIC2 and assigns 'mimic2v26_dat' as its
      tablespace (storage location).
 * It loads the MIMIC2 schema and the table definitions from the definition
   files.
 * If you have specified a range of subjects to be loaded using the -s and -e
   options, the MIMIC Importer determines which sets of subject-specific data
   include subjects to be loaded.  (If you have not chosen a range, the MIMIC
   Importer assumes you wish to load as many sets as you have downloaded.)
   For each such set:
    - If a tarball is available, it is unpacked.
    - If a directory containing unpacked flat files is available (either
      because it was just unpacked, or because it was left over from a previous
      run) the MIMIC importer loads any flat files within the range of selected
      subjects, and then removes these flat files (to avoid attempting to
      reload them in a later run).
 * To avoid unpacking the tarballs in a later run, the MIMIC Importer moves
   them into a subdirectory named 'tarballs' after unpacking each one.  If
   it's necessary to reload the database, they can be moved back into the
   top-level MIMIC Importer directory, where they will be accessible to the
   MIMIC Importer.

If you are interested in only a subset of the MIMIC II Clinical Database,
you can unpack the flat files for the subjects of interest, and remove any
others, as well as the tarballs, before running the MIMIC Importer.  In this
case, your MIMIC2 relational database will contain only the subjects of
interest to you;  you can always add more later on if your interests change.

If there were errors, you can try to correct them by modifying import.sh or
the files it reads.  Remove the tarballs and empty the database:
    rm -f *.tar.gz
    psql MIMIC2 -c "DROP SCHEMA mimic2v26 CASCADE"
before running import.sh again.

If for any reason you want to erase your MIMIC2 database (for example, to start
over) run the command
    dropdb MIMIC2
in a terminal window.  Although this makes the database very difficult to
recover, it does not erase the contents securely, which you must do if you plan
to dispose of the storage medium.

After running the MIMIC Importer successfully, you can safely remove the
MIMIC-Importer directory, and all its contents, if you wish to reclaim the
storage space it used.  It is also advisable to drop the PostgreSQL superuser
privileges assigned to your role (since it is easy to damage your database if
you work with superuser privileges).  To do this, acquire root and then
postgres privileges (as in step 4 in Appendix B), then run the command:
    psql -c "ALTER ROLE username WITH NOSUPERUSER;"
substituting your login name for "username".  If you wish to use the MIMIC
Importer to load more data later, restore the PostgreSQL superuser privileges
by acquiring root and postgres privileges again, and run:
    psql -c "ALTER ROLE username WITH SUPERUSER;"


Appendix D. Other scripts included in this package
--------------------------------------------------

In addition to the MIMIC Importer (import.sh) and the PostgreSQL setup
script (prep.sh), there are a few other scripts provided here:

'data-directory-name.sh'
    Shared by prep.sh and import.sh, this script locates the directory where
    PostgreSQL stores the default database cluster, which may vary on different
    platforms.

'exportid.sh'
    This is a fast and simple script that can create a set of flat files for
    a single subject.  Note that the format is not identical to that of the
    standard flat files (although it's very close -- see the comments in the
    script).  There are much faster ways to create a complete set of flat files
    for the entire database;  contact the authors if interested.

'reloadid.sh'
    Use this script to delete and then reload data for a given subject from
    a set of (original or revised) flat files.  When corrections are released,
    they are provided in the form of reloadable flat files.

'resetdb.sh'
    This script can be used to reset the PostgreSQL database cluster to its
    initial state;  it was useful while debugging the MIMIC Importer.  Since
    it destroys any PostgreSQL databases that you have created, don't use this
    script unless you are sure that you want to start over.


Appendix E.  Known limitations of this version of the MIMIC Importer
--------------------------------------------------------------------

PostgreSQL does not include builtin support for materialized views (see
the MIMIC II web site for a list of static tables that originated as
Oracle materialized views).  If MIMIC2 used as a read-only database (except
when adding new subjects), these tables do not pose a problem and may
be useful (which is the reason the MIMIC Importer loads them).  If the tables
upon which they are based change, however, these tables do not change, as they
would if they were views.

For possible workarounds, see
	http://wiki.postgresql.org/wiki/Materalized_Views

A future version may provide an option to load additional data without the need
for special PostgreSQL privileges, at a slower speed.


Appendix F. Changes from Version 2.5
--------------------------------------------------------------------

The following patient tables were added to version 2.6 that were not present in
version 2.5:
	COMORBIDITY_SCORES 
	DRGEVENTS 
	MICROBIOLOGYEVENTS 
        DEMOGRAPHIC_DETAIL 
	DEMOGRAPHICEVENTS
	PROCEDUREEVENTS

These tables are present in the on-line version of this database available
via the MIMIC II Explorer (Query Builder):
	WAVEFORM_METADATA
	WAVEFORM_SEG_SIG
	WAVEFORM_SEGMENTS
	WAVEFORM_SIGNALS
	WAVEFORM_TREND_SIGNALS
	WAVEFORM_TRENDS
The WAVEFORM_* tables contain references to MIMIC II Waveform Database
records that are being renamed during June 2011;  when the renaming is
complete, they will be made available with the next set of MIMIC II Clinical
Database flat files.

The following tables have been added to Definitions:
	D_DEMOGRAPHICITEMS
	D_CODEDITEMS
 	D_WAVEFORM_SIG *
* in the Query Builder database only
	

For a detailed list of all the changes please check the MIMIC II website.




