# Casting-Agency
Capstone Project for Full-Stack Udacity Nanodegree

pg_dump -U username dbname > dbexport.pgsql

psql -U username dbname < dbexport.pgsql

dropdb casting_test
createdb casting_test
psql casting_test < casting.pgsql
python -m unittest test_app.py