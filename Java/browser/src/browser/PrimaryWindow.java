package browser;

import java.awt.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.sql.SQLException;

import backend.DerbyDB;

public class PrimaryWindow extends JFrame {

	/**
	 * author @mblack884
	 * 
	 * This class and those it pulls in represent an early version of the GenreBrowser UI.
	 * The code is not yet well commented and will be re-organized more cleanly going forward.
	 * 
	 * As of 6/19/13: Basic searching, arff loading, & subtable creation are functional.
	 * 
	 * TODO:
	 * - Heading editor (text-fields in dialog box)
	 * - Prefs check at launch, write-out on close
	 * - Make sure prediction format is established so room can be made for page-level prediction later
	 * - Shift UI so all buttons are on the left, right will just be tables? (less confusing this way?)
	 * - Add all from prediction button?
	 * 
	 */
	
	DerbyDB connection;
	GridBagConstraints gbc;
	SearchResults results;
	SearchBox search;
	PredictionManager predict;
	JPanel top;
	String[] resCategories = {"HTID","Author","Title","Date"};
	String[] predCategories = {"HTID","Author","Title","Value"};
	
	public static void main(String[] args) {

		try {
			System.setProperty("derby.stream.error.logSeverityLevel", "3000");
			DerbyDB test = new DerbyDB("embedded","/Users/mike/Desktop/HathiBrowser/derbytest");
			new PrimaryWindow(test);
		} catch (SQLException e) {
			JOptionPane.showMessageDialog(null, "Problem connecting to Derby, please ensure all other\ninstances have been closed and restart.","Derby Error",JOptionPane.ERROR_MESSAGE);
			return;
		}
	}
	
	PrimaryWindow (DerbyDB conn) {
		setLayout(new GridLayout(0,1));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(900,600);
		search = new SearchBox(conn);
		predict = new PredictionManager(conn);
		results = new SearchResults(search.resModel,predict.targetModel);
		top = new JPanel();
		top.setLayout(new BorderLayout());
		top.add(search,BorderLayout.WEST);
		top.add(predict,BorderLayout.CENTER);
		add(top);
		add(results);
		setVisible(true);
	}

}
