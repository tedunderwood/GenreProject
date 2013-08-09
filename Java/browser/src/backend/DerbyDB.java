package backend;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;

public class DerbyDB {
	
	/**
	 * author: Mike Black @mlblack884
	 * NOTE: The load driver function was taken from the Apache Derby documentation.
	 * 
	 * This class serves as an interface to an Apache Derby database.  Currently, only the
	 * embedded driver is functional, but a networked driver should only require (in theory)
	 * a new constructor to pass login information along.  Once the new driver is loaded, the
	 * rest of the class should function normally without further changes.
	 * 
	 * When initializing a DerbyDB, enclose constructor in try/catch for SQLException and
	 * IOException.  SQLExceptions possible if there are multiple embedded connections to 
	 * the same database.  IOExceptions possible if source metatable file is unreadable 
	 * (or doesn't exist).
	 */
    
	private String database;
	private String driver;
    private String protocol = "jdbc:derby:";
    private Connection derbyconn;
	
    public DerbyDB (String framework, String location) throws SQLException {
    	/**
    	 * This constructor establishes a connection to an existing database at a given
    	 * location.
    	 */
    	database = location;
    	if (framework == "embedded") {
    		driver = "org.apache.derby.jdbc.EmbeddedDriver";
    	}
    	loadDriver();
    	
    	// Connect to database
    	derbyconn = DriverManager.getConnection(protocol + database);
    	System.out.println("Database successfully connected."); 
    }
    
    public DerbyDB (String framework, String location, String source) throws SQLException, IOException {
    	/**
    	 * This constructor creates a new database at a given location, establishes a 
    	 * connection, and populates it using a supplied data table. Supplied data source
    	 * must be in the expected 9 column, tab-delimited format produced from the
    	 * metaminer.py script: 
    	 * htid,volumeid,callnum,author,title,publisher,date,copy,subject
    	 */
    	database = location;
    	if (framework == "embedded") {
    		driver = "org.apache.derby.jdbc.EmbeddedDriver";
    	}
    	loadDriver();
    	
    	// Create database at location from source
    	System.out.println("Creating new database at " + location + ".");
		derbyconn = DriverManager.getConnection(protocol + database + ";create=true");
		System.out.println("Database successfully connected.");
		
		// Create tables for the various date scenarios
		System.out.println("Populating database using " + source);
		Statement s = derbyconn.createStatement();
		s.execute("CREATE TABLE COMPLETE (HTID VARCHAR(30) NOT NULL PRIMARY KEY, VOLNUM VARCHAR(16), CALLNUM VARCHAR(150), AUTHOR VARCHAR(100), TITLE VARCHAR(1500), PUBLISH VARCHAR(1000), DATE INT, COPY VARCHAR(100), SUBJECT VARCHAR(1500))");
		s.execute("CREATE TABLE RANGE (HTID VARCHAR(30) NOT NULL PRIMARY KEY, VOLNUM VARCHAR(16), CALLNUM VARCHAR(150), AUTHOR VARCHAR(100), TITLE VARCHAR(1500), PUBLISH VARCHAR(1000), DATE VARCHAR(9), COPY VARCHAR(100), SUBJECT VARCHAR(1500))");
		s.execute("CREATE TABLE FUZZY (HTID VARCHAR(30) NOT NULL PRIMARY KEY, VOLNUM VARCHAR(16), CALLNUM VARCHAR(150), AUTHOR VARCHAR(100), TITLE VARCHAR(1500), PUBLISH VARCHAR(1000), DATE VARCHAR(200), COPY VARCHAR(100), SUBJECT VARCHAR(1500))");
		
		// Index author/title columns since they are frequently searched
		s.execute("CREATE INDEX COMPLETEIDX ON COMPLETE (AUTHOR, TITLE)");
		s.execute("CREATE INDEX RANGEIDX ON RANGE (AUTHOR, TITLE)");
		s.execute("CREATE INDEX FUZZYIDX ON FUZZY (AUTHOR, TITLE)");

		// Create Prepared Statement strings for data insertion as table is read from file
		PreparedStatement psComplete = derbyconn.prepareStatement("INSERT INTO COMPLETE VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)");
		PreparedStatement psRange = derbyconn.prepareStatement("INSERT INTO RANGE VALUES (?,?,?,?,?,?,?,?,?)");
		PreparedStatement psFuzzy = derbyconn.prepareStatement("INSERT INTO FUZZY VALUES (?,?,?,?,?,?,?,?,?)");
		
		// Read in the table line by line and handle each entry accordingly
		InputStream inTable = new FileInputStream(source);
		BufferedReader inLines = new BufferedReader(new InputStreamReader(inTable, Charset.forName("UTF-8")));
		String line;
		String[] parts;

		while ((line = inLines.readLine()) != null){
			parts = line.split("\t");
			if (parts[6].length() == 4) {
				for(int i=0;i<9;i++){
					if (i != 6){
						psComplete.setString(i+1,parts[i]);
					}
					else {
						psComplete.setInt(i+1,Integer.parseInt(parts[i]));
					}
				}
				psComplete.executeUpdate();
			}
			else if (parts[6].length() <= 9 && parts[6].contains("-")){
				for(int i=0;i<9;i++) {
					psRange.setString(i+1,parts[i]);
				}
				psRange.executeUpdate();
			}
			else {
				for(int i=0;i<9;i++) {
					psFuzzy.setString(i+1,parts[i]);
				}
				psFuzzy.executeUpdate();
			}
		}
		
		inTable.close();
		inLines.close();
		s.close();
		psComplete.close();
		psRange.close();
		psFuzzy.close();
		
		System.out.println("Database populated.");
    	
    }

	public void close() throws SQLException {
		derbyconn.close();
		System.out.println("Database successfully closed.");
	}

    private void loadDriver() {
		/**
		 * NOTE: This function & documentation taken from Apache's Derby developer's guide. -mike
		 * 
		 *  The JDBC driver is loaded by loading its class.
		 *  If you are using JDBC 4.0 (Java SE 6) or newer, JDBC drivers may
		 *  be automatically loaded, making this code optional.
		 *
		 *  In an embedded environment, this will also start up the Derby
		 *  engine (though not any databases), since it is not already
		 *  running. In a client environment, the Derby engine is being run
		 *  by the network server framework.
		 *
		 *  In an embedded environment, any static Derby system properties
		 *  must be set before loading the driver to take effect.
		 */
		try {
			Class.forName(driver).newInstance();
			System.out.println("Loaded the appropriate JDBC Derby driver.");
		} catch (ClassNotFoundException cnfe) {
			System.err.println("\nUnable to load the JDBC driver " + driver);
			System.err.println("Please check your CLASSPATH.");
			cnfe.printStackTrace(System.err);
		} catch (InstantiationException ie) {
			System.err.println(
					"\nUnable to instantiate the JDBC driver " + driver);
			ie.printStackTrace(System.err);
		} catch (IllegalAccessException iae) {
			System.err.println(
					"\nNot allowed to access the JDBC driver " + driver);
			iae.printStackTrace(System.err);
		}
	}
 
    public String[][] query (String sql) throws SQLException {
    	/**
    	 * Accepts a SQL query as a String and returns the results as a matrix of Strings.
    	 * Currently, this method is hard-coded to return only four fields (htid, author, 
    	 * title, and date) and only for tables with normal dates.
    	 */
    	
    	ArrayList<String[]> results = new ArrayList<String[]>();
    	Statement s;
    	ResultSet rs;
		s = derbyconn.createStatement();
		rs = s.executeQuery(sql);
		String[] row = new String[4];
		// Derby results don't work like a normal array. You can't traverse easily via row index.  
		// Rows start at -1 and are advanced through in sequence. Each column is indexed by field name.
		while (rs.next()) {
			row[0] = rs.getString("HTID");
			row[1] = rs.getString("AUTHOR");
			row[2] = rs.getString("TITLE");
			row[3] = Integer.toString(rs.getInt("DATE"));
			results.add(row.clone());
		}
		rs.close();
		s.close();
		
    	return results.toArray(new String[results.size()][4]);
    }
    
    public String[] getRecord (String htid) throws SQLException {
    	/**
    	 * Retrieves a specific record (all 9 entries).  Should only return a single row since
    	 * HTID is set as a primary key, meaning there can only be one row in the database for
    	 * a particular HTID.
    	 */
    	String[] record = new String[9];
    	Statement s;
    	ResultSet rs;
    	s = derbyconn.createStatement();
    	rs = s.executeQuery("SELECT * FROM COMPLETE WHERE HTID = '" + htid +  "'");
    	rs.next();
    	record[0] = rs.getString("HTID");
    	record[1] = rs.getString("VOLNUM");
    	record[2] = rs.getString("CALLNUM");
    	record[3] = rs.getString("AUTHOR");
    	record[4] = rs.getString("TITLE");
    	record[5] = rs.getString("PUBLISH");
    	record[6] = Integer.toString(rs.getInt("DATE"));
    	record[7] = rs.getString("COPY");
    	record[8] = rs.getString("SUBJECT");
    	s.close();
    	rs.close();
    	return record;
    }
    
    public void createSubtable (String[] htids, String name) throws SQLException {
    	/**
    	 * Generates a subtable of entries with matching htids from all three tables using
    	 * using joins. In SQL you can do this in a single line, but Derby forces you to 
    	 * create the table of a specific columnsize first and then insert rows with matching
    	 * column sizes.  
    	 */
    	Statement s = derbyconn.createStatement();
    	s.execute("CREATE TABLE " + name.toUpperCase() + "(HTID VARCHAR(30))");
    	PreparedStatement ps = derbyconn.prepareStatement("INSERT INTO " + name.toUpperCase() + " VALUES(?)");
    	for(int i=0;i<htids.length;i++){ 
    		ps.setString(1,htids[i]);
    		ps.executeUpdate();
    	}
    	ps.close();
    	System.out.println("Prediction stored in derby.");
    	
    	s.execute("CREATE TABLE PREDICTION (HTID VARCHAR(30) NOT NULL PRIMARY KEY, VOLNUM VARCHAR(16), CALLNUM VARCHAR(150), AUTHOR VARCHAR(100), TITLE VARCHAR(1500), PUBLISH VARCHAR(1000), DATE INT, COPY VARCHAR(100), SUBJECT VARCHAR(1500))");
    	s.execute("INSERT INTO PREDICTION SELECT COMPLETE.* FROM COMPLETE JOIN " + name.toUpperCase() + " ON COMPLETE.HTID=" + name.toUpperCase() + ".HTID");

    	s.close();
    }
    
    public void command (String sql) throws SQLException{
    	/**
    	 * Use this method to pass commands to Derby which don't require output parsing.
    	 * It's a public method, but it's primary role is to serve as a primitive for 
    	 * more abstract method calls.
    	 */
    	Statement s;
    	s = derbyconn.createStatement();
    	s.execute(sql);
    	s.close();
    }
    
    public void dropTables() throws SQLException {
    	/**
    	 * Drops all tables that aren't part of the primary database (i.e., all subtables)
    	 */
    	String[] tables = getTables();
    	for(int i=0;i<tables.length;i++){
    		System.out.println("Dropping table " + tables[i] + ".");
    		command("DROP TABLE " + tables[i]);
    	}
    	
    }
    
    private String[] getTables() throws SQLException {
    	/**
    	 * Returns the filtered results of a SQL query for all table names.  The three tables
    	 * that comprise the primary metadata database are filtered so they won't be dropped. 
    	 */
    	ArrayList<String> results = new ArrayList<String>();
    	Statement s;
    	ResultSet rs;
    	s = derbyconn.createStatement();
    	rs = s.executeQuery("SELECT TABLENAME FROM SYS.SYSTABLES WHERE TABLETYPE='T'");
    	while(rs.next()) {
    		String tablename = rs.getString("TABLENAME").trim();
    		if(!tablename.equals("COMPLETE") && !tablename.equals("RANGE") && !tablename.equals("FUZZY")) {
    			results.add(tablename);
    		}
    	}
    	rs.close();
    	s.close();
    	return results.toArray(new String[results.size()]);	
    }
}
