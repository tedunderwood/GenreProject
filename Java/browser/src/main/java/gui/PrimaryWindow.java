package gui;

import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import javax.swing.*;
import java.sql.SQLException;
import backend.DerbyDB;
import backend.Preferences;

public class PrimaryWindow extends JFrame {

	/**
	 * author: Mike Black @mblack884
	 * 
	 * Functionally speaking, this class is the GenreBrowser.  It loads all of the core
	 * components in sequence, passing in the backend objects (DerbyDB and Preferences)
	 * to primary GUI components (PredictionManager, SearchBox, SearchResults).  
	 * 
	 */
	
	DerbyDB derby;
	Preferences prefs;
	SearchResults results;
	SearchBox search;
	PredictionManager predict;
	JPanel top,bottom;
	
	public static void main(String[] args) {
		DerbyDB database;
		// Derby log level of 3000 is pretty verbose, but I chose it because it records the
		// complete command of any SQL query that produced an error.
		System.setProperty("derby.stream.error.logSeverityLevel", "3000");
		Preferences p = new Preferences(Preferences.DEFAULT_PREF_FILE);
		try {
			if (!p.exists()) {
				database = new DerbyDB("embedded",p.getDerbyDir(),p.getSource());
			} else {
				database = new DerbyDB("embedded",p.getDerbyDir());
			}
			new PrimaryWindow(database,p);
		} catch (SQLException e) {
			JOptionPane.showMessageDialog(null, "Problem connecting to Derby, please ensure all other\ninstances have been closed and restart.","Derby Error",JOptionPane.ERROR_MESSAGE);
			return;
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Error populating Derby database. Please make sure\nthe file seed file is accessible.","Derby Error",JOptionPane.ERROR_MESSAGE);
			return;
		}
	}
	
	PrimaryWindow (DerbyDB db, Preferences p) {
		/**
		 * This is essentially the main program.  The main above starts two more core
		 * backend components.  The core GUI objects are intialized here and then the
		 * main window is displayed.  Layout-wise, the main window is subdivided into
		 * two equal panels using the Grid Layout, and the bottom is subdivided using
		 * Border with SearchBox taking the smaller West space and SearchResults the
		 * larger Center space.
		 */
		prefs = p;
		derby = db;
		setLayout(new GridLayout(0,1));
		setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		defineListeners();
		setSize(900,600);
		search = new SearchBox(derby);
		predict = new PredictionManager(derby,prefs);
		results = new SearchResults(search.resultsModel,predict.targetModel,derby);
		bottom = new JPanel();
		bottom.setLayout(new BorderLayout());
		bottom.add(search,BorderLayout.WEST);
		bottom.add(results,BorderLayout.CENTER);
		add(predict);
		add(bottom);
		setVisible(true);
	}
	
	private void defineListeners() {
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				/**
				 * This Window Listener should behave like those in most other data editting programs.
				 * If data has been modified without save, it will prompt users to save.  If users select
				 * yes, then data will be saved and program closed.  If they select no, then any changes
				 * since the last save will be dismissed and program will close.  If they select cancel,
				 * then the program will remain open.  As far as changes go, this Listener only checks 
				 * for changes to the target prediction.
				 */
				if (predict.getSaveState()) {
					int response = JOptionPane.showConfirmDialog(null,"Target prediction has been modified. Save on exit?","Exit without Saving",JOptionPane.YES_NO_CANCEL_OPTION);
					switch (response) {
						case JOptionPane.YES_OPTION:	
							if (predict.doSave()) {
								doClose();
							} else {
								// If the user accidently closes the save file dialog, this will remind them that they still need to save.
								JOptionPane.showMessageDialog(null, "Document was not saved successfully by user. Program close halted.","Save Error",JOptionPane.WARNING_MESSAGE);
							}
							break;					
						case JOptionPane.NO_OPTION:
							doClose();
							break;
						case JOptionPane.CANCEL_OPTION:
							break;
					}
				} else {
					doClose();
				}
			}
		});
	}
	
	private void doClose() {
		/**
		 * Program close sequence.  Any subtables created during this session must be dropped
		 * so that there will not be a problem later on if users decide to load the same
		 * source ARFF during a later session.  Preferences must also be written to disk. If
		 * for any reason this sequence is interrupted, program close will be aborted.
		 */
		try {
			derby.dropTables();
			derby.close();
			prefs.writePrefs();
		} catch (SQLException e) {
			JOptionPane.showMessageDialog(null, "Problem disconnecting from Derby database. Please make\nsure files have not been moved or corrupted.","Derby Error",JOptionPane.ERROR_MESSAGE);
		}
		System.exit(0);
	}

}
