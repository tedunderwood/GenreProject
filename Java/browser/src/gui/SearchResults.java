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
	/*
	 * TODO:
	 * - Pass in table model for predictions
	 * - Write button logic for adding to predictions
	 * - Write record display logic (setup a new dialog class or pass to optionpane?)
	 */
	
	private JScrollPane rcontainer;
	private JTable rtable;
	private JButton add, view;
	private JPanel buttons;
	private RecordViewer showrecord;
	
	// Referenced from other classes
	private PredictionTableModel tmodel;
	private DerbyDB derby;
	
	public SearchResults (ResultsTableModel results, PredictionTableModel predictions, DerbyDB conn) {
		derby = conn;
		tmodel = predictions;
		rtable = new JTable(results);
		rcontainer = new JScrollPane(rtable);
		add = new JButton("Add to prediction");
		view = new JButton("View complete record");
		buttons = new JPanel();
		drawGUI();
		defineButtons();
	}
	
	private void drawGUI() {
		setBorder(new EmptyBorder(5, 10, 10, 10));
		setLayout(new BorderLayout());
		rtable.setAutoCreateColumnsFromModel(false);
		rtable.setAutoResizeMode(JTable.AUTO_RESIZE_NEXT_COLUMN);
		rtable.getColumnModel().getColumn(0).setPreferredWidth(180);
		rtable.getColumnModel().getColumn(1).setPreferredWidth(140);
		rtable.getColumnModel().getColumn(2).setPreferredWidth(350);
		rtable.getColumnModel().getColumn(3).setPreferredWidth(40);
		rtable.getColumnModel().getColumn(3).setMinWidth(40);
		rcontainer.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
		add(rcontainer, BorderLayout.CENTER);
		buttons.setLayout(new BoxLayout(buttons,BoxLayout.X_AXIS));
		buttons.add(Box.createHorizontalGlue());
		buttons.add(add);
		buttons.add(view);
		buttons.add(Box.createHorizontalGlue());
		add(buttons, BorderLayout.SOUTH);
		
	}
	
	private String[] getSelection(int row) {
		String[] record = new String[rtable.getModel().getColumnCount()];
		for(int i=0;i<record.length;i++){
			record[i] = rtable.getModel().getValueAt(row, i).toString();
		}
		return record;
	}
	
	private void addRecord(String[] record) {
		/**
		 * Passes the row vector to the ResultsTableModel. 
		 */		
		tmodel.addPrediction(record[ResultsTableModel.HTID_COL],record[ResultsTableModel.AUTHOR_COL],record[ResultsTableModel.TITLE_COL],record[ResultsTableModel.DATE_COL], "--");
	}
	
	private void defineButtons() {
		add.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int[] selected = rtable.getSelectedRows();
				for (int i=0;i<selected.length;i++) {
					addRecord(getSelection(selected[i]));
				}
			}
		});
		
		view.addActionListener(new ActionListener () {
			public void actionPerformed(ActionEvent e) {
				int[] selected = rtable.getSelectedRows();
				if (selected.length == 1){
					try {
						String[] record;
						record = derby.getRecord(rtable.getModel().getValueAt(selected[0], 0).toString());
						showrecord = new RecordViewer(record);
						showrecord.setVisible(true);
					} catch (SQLException e1) {
						JOptionPane.showMessageDialog(null, "Database query cannot be processed.\n\nConsult derby.log for details.","Search Error",JOptionPane.WARNING_MESSAGE);
					}
						
				} else {
					JOptionPane.showMessageDialog(null, "Can only view one record at a time.","Input Error",JOptionPane.WARNING_MESSAGE);
				} 
			}
		});
	}
	
}
