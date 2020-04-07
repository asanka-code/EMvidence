

# clearing the 'data' directory 
rm -r data/*
touch data/placeholder.txt

# restore the database to the distribution state
rm emvidence-database.db
cp emvidence-database.db.default emvidence-database.db

# remove the '*.pyc' files
find . -name "*.pyc" -type f -delete

