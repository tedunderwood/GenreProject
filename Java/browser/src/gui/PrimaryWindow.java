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
	 * author @mblack884
	 * 
	 * This class and those it pulls in represent an early version of the GenreBrowser UI.
	 * The code is not yet well commented and will be re-organized more cleanly going forward.
	 * 
	 * Working as of 7/13/13:
	 * - Preferences class loads/saves database location on program start/exit
	 * - Derby database creation from metadata.txt if no database or preferences file are found
	 * - Loading/saving of predictions
	 * - Database searching (complete & limited to source prediction records)
	 * - Adding results to target prediction from search or from source prediction
	 * - Header editing for target prediction
	 * - Set records in target prediction as match/miss
	 * 
	 * TODO:
	 * - Migrate to MAVEN
	 * - Page range/parts editor
	 * - Complete documentation & comments
	 * - Make sure object names follow uniform naming scheme across classes
	 * - Uniform error dialog class?
	 *  
	 * 7/15/13 & onward: UI tweaks, adjustments towards better modularization, debugging/userproofing
	 * 
	 * KNOWN BUGS:
	 * - Header editor throws error if target arff has not been created
	 * - The Window Closing listener does not activate if user closes from the Mac application menu 
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
		System.setProperty("derby.stream.error.logSeverityLevel", "3000");
		//TODO: Move exception handling for preferences to here?
		Preferences p = new Preferences();
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
		prefs = p;
		derby = db;
		setLayout(new GridLayout(0,1));
		setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		defineClose();
		setSize(900,600);
		search = new SearchBox(derby);
		predict = new PredictionManager(derby);
		results = new SearchResults(search.rmodel,predict.tmodel,derby);
		bottom = new JPanel();
		bottom.setLayout(new BorderLayout());
		bottom.add(search,BorderLayout.WEST);
		bottom.add(results,BorderLayout.CENTER);
		add(predict);
		add(bottom);
		setVisible(true);
	}
	
	private void defineClose() {
		addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				if (predict.getSaveState()) {
					int response = JOptionPane.showConfirmDialog(null,"Target prediction has been modified. Save on exit?","Exit without Saving",JOptionPane.YES_NO_CANCEL_OPTION);
					switch (response) {
						case JOptionPane.YES_OPTION:	
							if (predict.doSave()) {
								doClose();
							} else {
								//TODO: Error message
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
