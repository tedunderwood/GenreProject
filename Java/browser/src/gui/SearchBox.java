package gui;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.SQLException;
import java.util.ArrayList;

import backend.DerbyDB;
import backend.ResultsTableModel;

public class SearchBox extends JPanel {
	/**
	 * Constructor requires that a DerbyDB database be specified.
	 * TODO: Also require a list model? (To load results into for display in other class)
	 */
	
	private JLabel authorL, titleL,htidL,beforeL,afterL;
	private JTextField authorF, titleF, htidF,beforeF,afterF;
	private JPanel commands;
	private JButton submit, clear;
	private JCheckBox subset;
	ResultsTableModel rmodel;
	
	// References to external structures
	private DerbyDB derby;
	
	// Search interface constants
	final private String[] COL_NAMES = {"HTID","Author","Title","Date"};
	final private int MIN_SEARCH = 2;
	
	public SearchBox (DerbyDB conn) {
		
		// Override default settings in table model to forbid users from editing cells because Java doesn't provide this option natively for some reason
		rmodel = new ResultsTableModel();
		
		// Store reference to DerbyDB internally for all future search actions
		derby = conn;
		
		//Setup UI objects
		drawGUI();
		defineButtons();
				
	}
	
	private void drawGUI () {
		GridBagConstraints labels,fields,full;
		setBorder(new EmptyBorder(10, 10, 5, 5));
		Dimension textbox = new Dimension(175,30);
		
		// Set universal layout properties
		setLayout(new GridBagLayout());
		full = new GridBagConstraints();
		full.gridwidth = 4;
		
		// Set universal label & form properties
		labels = new GridBagConstraints();
		labels.gridwidth = 1;
		labels.gridx = 0;
		fields = new GridBagConstraints();
		fields.gridwidth = 3;
		fields.gridx = 1;
		//fields.insets = new Insets(3,3,3,3);
		
		// Set remaining properties for each label and add to layout
		authorL = new JLabel("Author:");
		labels.gridy = 0;
		add(authorL,labels);
		titleL = new JLabel("Title:");
		labels.gridy = 1;
		add(titleL,labels);
		htidL = new JLabel("HTID:");
		labels.gridy = 2;
		add(htidL,labels);
		beforeL = new JLabel("Before:");
		labels.gridy = 3;
		add(beforeL,labels);
		afterL = new JLabel("After:");
		labels.gridy = 4;
		add(afterL,labels);
		
		// Set remaining properties for each form and add to layout
		authorF = new JTextField(null);
		authorF.setPreferredSize(textbox);
		fields.gridy = 0;
		add(authorF,fields);
		titleF = new JTextField(null);
		titleF.setPreferredSize(textbox);
		fields.gridy = 1;
		add(titleF,fields);
		htidF = new JTextField(null);
		htidF.setPreferredSize(textbox);
		fields.gridy = 2;
		add(htidF,fields);
		beforeF = new JTextField(null);
		beforeF.setPreferredSize(textbox);
		fields.gridy = 3;
		add(beforeF,fields);
		afterF = new JTextField(null);
		afterF.setPreferredSize(textbox);
		fields.gridy = 4;
		add(afterF,fields);
		
		// Create buttons in universal "full row" constraints but use nested grid for evenly split button sections
		full.gridx = 0;
		full.gridy = 5;
		subset = new JCheckBox("Limit search to predictions");
		add(subset,full);
		commands = new JPanel();
		commands.setLayout(new GridLayout(1,2));
		submit = new JButton("Search");
		clear = new JButton("Clear");
		commands.add(submit);
		commands.add(clear);
		full.gridy = 6;
		add(commands,full);
	}
	
	private void defineButtons() {
		
		// Submit query (check to see if search fields are used correctly, then generate SQL and pass to Derby)
		submit.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				// TODO: Write a search check function that returns true/false to replace lengthy conditional  
				if (allowSearch()) {	
					String sql = parseSearchSQL(authorF.getText(),titleF.getText(),htidF.getText(),beforeF.getText(),afterF.getText(),subset.isSelected());
					String[][] results;
					try {
						results = derby.query(sql);
						for(int i=0;i<results.length;i++){
							addRecord(results[i]);
						}
					} catch (SQLException badQuery) {
						// TODO More specific error message?
						JOptionPane.showMessageDialog(null, "Database query cannot be processed.\n\nConsult derby.log for details.","Search Error",JOptionPane.WARNING_MESSAGE);
					}
				} else {
					JOptionPane.showMessageDialog(null, "Cannot perform search. Fields are empty or dates are not in expected format","Search Error",JOptionPane.PLAIN_MESSAGE);
				}
			}
		});
		
		// Clear search fields & reset prediction subset flag to inactive
		clear.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				titleF.setText(null);
				authorF.setText(null);
				htidF.setText(null);
				afterF.setText(null);
				beforeF.setText(null);
				subset.setSelected(false);
				rmodel.setRowCount(0);
			}
		});
	}
	
	private String parseSearchSQL (String author, String title, String htid, String before, String after, boolean limit) {
		ArrayList<String> clauses = new ArrayList<String>();
		String query = "";
		String database;
		// Table selection
		if (limit) {
			database = "PREDICTION";
		} else {
			database = "COMPLETE";
		}	
		// Clause builder
		if (author.length() >= MIN_SEARCH) {
			clauses.add(" LOWER(AUTHOR) LIKE LOWER('%" + author + "%')");
		}
		if (title.length() >= MIN_SEARCH) {
			clauses.add(" LOWER(TITLE) LIKE LOWER('%" + title + "%')");
		}
		
		if (htid.length() >= MIN_SEARCH) {
			clauses.add(" LOWER(HTID) LIKE LOWER('%" + htid + "%')");
		}
		if (after.trim().length() == 4) {
			clauses.add(" DATE>=" + after.trim());
		}
		if (before.trim().length() == 4) {
			clauses.add(" DATE<=" + before.trim());
		}		
		String[] builder = clauses.toArray(new String[clauses.size()]);		
		for (int i=0;i<builder.length;i++){
			if (i>0){
				query += " AND";
			}
			query += builder[i];
		}		
		return "SELECT HTID, TITLE, AUTHOR, DATE FROM " + database + " WHERE" + query + " ORDER BY DATE ASC";
	}
	
	private boolean allowSearch () {		
		// First check date fields
		if ((beforeF.getText().length() != 4 && beforeF.getText().length() != 0) || (afterF.getText().length() != 4 && afterF.getText().length() != 0)) {
			return false;
		}
		else if (authorF.getText().length() < MIN_SEARCH && titleF.getText().length() < MIN_SEARCH && htidF.getText().length() < MIN_SEARCH) {
			return false;
		}
		else {
			return true;
		}		
	}
	
	private void addRecord(String[] record) {
		rmodel.addResult(record[ResultsTableModel.HTID_COL], record[ResultsTableModel.AUTHOR_COL], record[ResultsTableModel.TITLE_COL], record[ResultsTableModel.DATE_COL]);
	}

}
