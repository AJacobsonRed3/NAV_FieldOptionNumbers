# NAV_FieldOptionNumbers
Get NAv Field and Option Numbers into a SQL Table for query use

I've written a detailed blog post which goes through this step by step.
Please note:  The programs (other than the simple SQL to build the table) are written in Python.
I am working with Python 3.7.
You must make sure that you have access to the following on Python
numpy
pandas
pyodbc
sqlalchemy
I believe that everything else I reference comes with the standard install.

To build the NAVFieldNames and NAVFieldOptions
1)	Create the two new tables in your reporting database.
	The script is 010 - Tables to Store Field and Option Data.sql.
2)	Run: 100 - Build NAVFieldNames NAVFieldOptions.py in Python.

The other scripts here can be used to better understand how everything works.  Please read the blog post for more information.	
	
