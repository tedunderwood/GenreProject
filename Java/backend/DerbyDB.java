package backend;

import java.nio.charset.Charset;
import java.sql.*;
import java.util.ArrayList;
import java.io.*;

public class DerbyDB {
	
	/*
	 * TODO:
	 * - Proper exception handling (using eclipse's adhoc try/catch autoforms for now)
	 * - More efficient way to get from ResultSet to String[][]?
	 * - Possibly index author/title columns at creation for faster retrieval?
	 */
    
	private String database;
	private String driver;
    private String protocol = "jdbc:derby:";
    private Connection derbyconn;
	
    public DerbyDB (String framework, String location) {
    	/*
    	 * This constructor establishes a connection to an existing database at a given location.
    	 */
    	database = location;
    	if (framework == "embedded") {
    		driver = "org.apache.derby.jdbc.EmbeddedDriver";
    	}
    	loadDriver();
    	// Test connection
    	try {
    		derbyconn = DriverManager.getConnection(protocol + database);
    		System.out.println("Database successfully connected.");
    	} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
    }
    
    public DerbyDB (String framework, String location, String source) {
    	/*
    	 * This constructor creates a new database at a given location, establishes a connection, and populates it using a supplied data table.
    	 * 
    	 * Supplied data source must be in the expected 9 column, tab-delimited format produced from the metaminer.py script (htid,volumeid,callnum,author,title,publisher,date,copy,subject)
    	 */
    	database = location;
    	if (framework == "embedded") {
    		driver = "org.apache.derby.jdbc.EmbeddedDriver";
    	}
    	loadDriver();
    	// Create database at location from source
    	try {
			// In production versions, include something to check to see if database exists and create it if not.
			derbyconn = DriverManager.getConnection(protocol + database + ";create=true");
			System.out.println("Database successfully connected.");
			
			// Create tables for the various date scenarios
			System.out.println("Populating database using " + source);
			
			Statement s = derbyconn.createStatement();
			s.execute("CREATE TABLE COMPLETE (HTID VARCHAR(16), VOLNUM VARCHAR(16), CALLNUM VARCHAR(50), AUTHOR VARCHAR(100), TITLE VARCHAR(500), PUBLISH VARCHAR(300), DATE INT, COPY VARCHAR(50), SUBJECT VARCHAR(500))");
			s.execute("CREATE TABLE RANGE (HTID VARCHAR(16), VOLNUM VARCHAR(16), CALLNUM VARCHAR(50), AUTHOR VARCHAR(100), TITLE VARCHAR(500), PUBLISH VARCHAR(300), DATE VARCHAR(9), COPY VARCHAR(50), SUBJECT VARCHAR(500))");
			s.execute("CREATE TABLE FUZZY (HTID VARCHAR(16), VOLNUM VARCHAR(16), CALLNUM VARCHAR(50), AUTHOR VARCHAR(100), TITLE VARCHAR(500), PUBLISH VARCHAR(300), DATE VARCHAR(50), COPY VARCHAR(50), SUBJECT VARCHAR(500))");

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
			
    	} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
    	
    }

	public void close() {
		try {
			derbyconn.close();
			System.out.println("Database successfully closed.");
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

    private void loadDriver() {
		/*
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
			System.out.println("Loaded the appropriate driver");
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
 
    public String[][] Query (String sql) {
    	ArrayList<String[]> results = new ArrayList<String[]>();
    	Statement s;
    	ResultSet rs;
		try {
			s = derbyconn.createStatement();
			rs = s.executeQuery(sql);
			String[] row = new String[4];
			while (rs.next()) {
				row[0] = rs.getString("HTID");
				row[1] = rs.getString("AUTHOR");
				row[2] = rs.getString("TITLE");
				row[3] = Integer.toString(rs.getInt("DATE"));
				results.add(row.clone());
			}
			rs.close();
			s.close();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
    	return results.toArray(new String[results.size()][4]);
    }
}
