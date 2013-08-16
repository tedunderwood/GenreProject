package gui;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.SQLException;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import backend.DerbyDB;
import backend.PredictionTableModel;
import backend.ResultsTableModel;

public class SearchResults extends JPanel {
	/**
	 * This class mostly just displays the results of SQL queries.  It also acts
	 * as an interface between the search and prediction portions of the progra by
	 * passing data from the ResultsTable to the PredictionTable.
	 */
	
	private JScrollPane resultsScroll;
	private JTable resultsTable;
	private JButton add, view;
	private JPanel buttons;
	private RecordViewer recordView;
	
	// References to external data structures
	private PredictionTableModel targetModel;
	private DerbyDB derby;
	
	public SearchResults (ResultsTableModel results, PredictionTableModel predictions, DerbyDB conn) {
		/**
		 * Basic constructor that stores references to Derby and the prediction manager's 
		 * table.  It also initializes the table container for search results and passes
		 * the search table model into it.
		 */
		derby = conn;
		targetModel = predictions;
		resultsTable = new JTable(results); // The ResultsTableModel isn't stored as its own reference here because this class shouldn't directly access it
		resultsScroll = new JScrollPane(resultsTable);
		add = new JButton("Add to prediction");
		view = new JButton("View complete record");
		buttons = new JPanel();
		drawGUI();
		defineListeners();
	}
	
	private void drawGUI() {
		/**
		 * Initializes all of the graphics objects and positions them within nested
		 * panels/layout managers.  Panels used by groups are objects are initialized
		 * in the same section as those objects.
		 */
		
		setBorder(new EmptyBorder(5, 10, 10, 10));
		setLayout(new BorderLayout());
		resultsTable.setAutoCreateColumnsFromModel(false);
		resultsTable.setAutoResizeMode(JTable.AUTO_RESIZE_NEXT_COLUMN);
		resultsTable.getColumnModel().getColumn(0).setPreferredWidth(180);
		resultsTable.getColumnModel().getColumn(1).setPreferredWidth(140);
		resultsTable.getColumnModel().getColumn(2).setPreferredWidth(350);
		resultsTable.getColumnModel().getColumn(3).setPreferredWidth(40);
		resultsTable.getColumnModel().getColumn(3).setMinWidth(40);
		resultsScroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
		add(resultsScroll, BorderLayout.CENTER);
		buttons.setLayout(new BoxLayout(buttons,BoxLayout.X_AXIS));
		buttons.add(Box.createHorizontalGlue());
		buttons.add(add);
		buttons.add(view);
		buttons.add(Box.createHorizontalGlue());
		add(buttons, BorderLayout.SOUTH);
		
	}
	
	private String[] getSelection(int row) {
		/**
		 * This method pulls the record data from the ResultsTableModel, primarily for
		 * passing it to the PredictionManager without needing to do another
		 * SQL query but also for passing to the RecordViewer.
		 */
		String[] record = new String[resultsTable.getModel().getColumnCount()];
		for(int i=0;i<record.length;i++){
			record[i] = resultsTable.getModel().getValueAt(row, i).toString();
		}
		return record;
	}
	
	private void addRecord(String[] record) {
		/**
		 * Passes htid, author, and title for a record to the Prediction Manager's table
		 * along with some empty data in prediction fields that wouldn't be in DerbyDB. 
		 */		
		targetModel.addPrediction(record[ResultsTableModel.HTID_COL],record[ResultsTableModel.AUTHOR_COL],record[ResultsTableModel.TITLE_COL],record[ResultsTableModel.DATE_COL], "--");
	}
	
	private void defineListeners() {
		/**
		 * Sets all the button commands (ActionListeners).  This function creates them as
		 * anonymous subclasses.  It's hacky, and for a bigger program it would probably
		 * be better to define them each separately.  The overall function of each button
		 * is described in comments preceding the ActionListener definitions.
		 */
		add.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				/**
				 * This button adds selected search results to the target prediction.
				 */
				int[] selected = resultsTable.getSelectedRows();
				for (int i=0;i<selected.length;i++) {
					addRecord(getSelection(selected[i]));
				}
			}
		});
		
		view.addActionListener(new ActionListener () {
			public void actionPerformed(ActionEvent e) {
				/**
				 * If users have selected a single record, they button issues a SQL
				 * query to get all 9 fields for a record and passes them to a newly 
				 * initialized RecordViewer.
				 */
				int[] selected = resultsTable.getSelectedRows();
				if (selected.length == 1){
					try {
						String[] record;
						record = derby.getRecord(resultsTable.getModel().getValueAt(selected[0], 0).toString());
						recordView = new RecordViewer(record);
						recordView.setVisible(true);
					} catch (SQLException e1) {
						JOptionPane.showMessageDialog(null, "Database query cannot be processed.\n\nConsult derby.log for details.","Search Error",JOptionPane.WARNING_MESSAGE);
					}
						
				} else {
					JOptionPane.showMessageDialog(null, "Can only view one record at a time.","Selection Error",JOptionPane.WARNING_MESSAGE);
				} 
			}
		});
	}
	
}
