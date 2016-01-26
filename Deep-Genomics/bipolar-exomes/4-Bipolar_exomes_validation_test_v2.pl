#!/usr/bin/perl -T
###################################################################
#	Validations for Bipolar_exomes, 2015
#	Number of rows: 500 + 1 header row
#	Number of columns: 4
#	Columns 2-3 range: 0+
###################################################################

use strict;
my $num_rows = 500; # excluding header
my $num_columns = 4;

my $filename = $ARGV[0];
if ($filename =~ /^([#%@=+a-z0-9_.\-\/\\]+)$/i) {
    $filename = $1;
} else {
    die("filename too complex");
}

open (IFILE, "$filename") or die("Cannot open input file: $!");
my @contents = <IFILE>;
close(IFILE);

my @errors = ();
push(@errors, "The number of lines do not match the template\n") if (@contents != $num_rows+1);

my @num_attempted = (0) x $num_columns;

my $cnt =1;
while ($cnt < @contents) {
    chomp($contents[$cnt]);
    my @cols = split("\t",$contents[$cnt++]);
    push(@errors,"The number of columns is less than the allowed number for $cols[0]. Please indicate the empty columns with '*'.\n") if (@cols < $num_columns);
    push(@errors,"The number of columns is greater than the allowed number for $cols[0]. Tabs can only be used as column separators.\n") if (@cols > $num_columns);

    for (my $i=0; $i<$num_columns; $i++) {
	$num_attempted[$i]++ if ($cols[$i] ne "*");
	if ($cols[$i] eq "") {
	    push(@errors,"Column $i cannot be empty for $cols[0] on line number $cnt; leave a '*' to indicate empty columns.\n");
	}
    }

    if ((($cols[1] < 0) || ($cols[1] > 1) || ($cols[1] !~ /^[+]?([.]\d+|\d+([.]\d+)?)$/)) && !($cols[1] eq "*")) {
	push(@errors,"disease_status '$cols[1]' must be [0-1] for $cols[0] on line number $cnt\n");
    }

    if ((($cols[2] < 0) || ($cols[2] !~ /^[+]?([.]\d+|\d+([.]\d+)?)$/)) && !($cols[2] eq "*")) {
	push(@errors,"disease_status s.d. '$cols[2]' must be >=0 for $cols[0] on line number $cnt\n");
    }
}

if ((($num_attempted[1] > 0) ||
     ($num_attempted[2] > 0)) && (($num_attempted[1] != $num_rows) ||
				  ($num_attempted[2] != $num_rows))) {
    push(@errors,"You must make all or no predictions for disease_status and s.d.\n");
    push(@errors,"You made $num_attempted[1] disease_status predictions and $num_attempted[2] s.d. predictions.\n");
}

if (($num_attempted[1]==0) && ($num_attempted[2]==0)) {
    push(@errors,"You didn't make any predictions; did you accidently submit the template?\n");
}

if (@errors > 0) {
    print "Validation failed with errors:\n";
    print @errors;
    exit 1;
} else {
    print "Validation passed with no errors.\n";
    if ((-x "/usr/bin/md5sum") && (-x "/usr/bin/cut")) {
	print "MD5 hash for your file is ";
	$ENV{PATH} = "";
	system ("/usr/bin/md5sum $filename | /usr/bin/cut -c 1-32");
	if ((-r "cagi.txt") && (-x "/bin/cat")) {
	    print "Receipt code for your file is ";
	    system ("/bin/cat cagi.txt $filename | /usr/bin/md5sum | /usr/bin/cut -c 1-32");
	}
    }
    exit 0;
}
