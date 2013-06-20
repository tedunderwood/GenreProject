package browser;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;

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
	
	// Referenced from other classes
	private DefaultTableModel prediction;
	
	public SearchResults (DefaultTableModel results, DefaultTableModel preModel) {
		prediction = preModel;
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
		String[] newPredict = new String[record.length+1];
		newPredict[0] = "--";
		for (int i=0;i<record.length;i++) {
			newPredict[i+1] = record[i];
		}
		prediction.addRow(newPredict);
	}
	
	private void defineButtons() {
		add.addActionListener(
			new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					int mode = rtable.getSelectionModel().getSelectionMode();
					if (mode == ListSelectionModel.SINGLE_SELECTION) {
						int selected = rtable.getSelectedRow();
						if (selected >= 0){
							addRecord(getSelection(selected));
						}
					} else {
						int[] selected = rtable.getSelectedRows();
						for (int i=0;i<selected.length;i++) {
							addRecord(getSelection(selected[i]));
						}
					}
				}
			}
		);
	}
	

}
