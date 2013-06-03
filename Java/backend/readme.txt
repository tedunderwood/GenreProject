6/3/13 - mike
For the time being, I'm going to store all of the classes I write to handle the data sources available to users of the browser tool in this folder.  Right now there is just the DerbyDB interface (and its dependency).  I'll refine the organization as I upload more pieces of the browser tool.

DerbyDB
This is a class written using the Derby API to handle basic operations with the large metadata table that was generated during an earlier phase of the project.  Currently, it is capable of:
- connecting to an existing, local database
- creating a new database and populating it using metatable.txt (or a similar structured table)
- filtering metatable.txt entries with ranges or fuzzy dates into separate tables within the Derby database so that queries can be made based on publication date and/or results ordered by date
- issuing SQL queries and returning the results as a String[][] matrix

Databases are connected to (or created) using the constructors.  In addition to specifying a local database or a seed metatable.txt file, a framework must be also be specified.  For now, this should always be "embedded".  Changes to the constructors to setup a networked connection shouldn't affect the rest of the methods.

To use an instance of DerbyDB to perform a search, the object will need to be passed into the object that deals with user input.  The user input object will then need to parse search fields into an SQL string for DerbyDB.  I left the query method open-ended, accepting just an SQL command as a String so that there wouldn't be any limitations on searches in DerbyDB.

This class will not work unless Apache's derby.jar is included in the CLASSPATH!

TODO: 
- Proper exception handling
- A better way of getting from Derby's awkward ResultSet to a String[][] (needed by Java's table models)
- Consider indexing author/title columns in Derby.  Set HTid as primary key?
