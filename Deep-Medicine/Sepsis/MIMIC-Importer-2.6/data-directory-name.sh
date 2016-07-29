psql postgres -c "SHOW ALL;" | grep data_directory | cut -d "|" -f 2 |sed "s/ //g"
