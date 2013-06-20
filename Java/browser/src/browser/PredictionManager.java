package browser;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.sql.SQLException;
import java.util.ArrayList;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;
import backend.ARFF;
import backend.DerbyDB;

public class PredictionManager extends JPanel {
	DefaultTableModel targetModel;
	private DerbyDB derby;
	private ARFF source,target;
	private JPanel files, values;
	private JScrollPane tcontainer;
	private JTable ttable;
	private JTextField sname,tname;
	private JButton tsave, sload, newDB, posValue, negValue,theader,clear;
	//private JDialog heditor;
	private JLabel slabel,tlabel;
	private Boolean modified;
	private File tfile;
	private FileNameExtensionFilter arffonly;
	
	//Interface construction constants
	final private String[] COL_NAMES = {"Prediction","HTID","Author","Title","Date"};
	
	public PredictionManager(DerbyDB conn) {
		// Override default settings in table model to forbid users from editing cells because Java doesn't provide this option natively for some reason
		targetModel = new DefaultTableModel(COL_NAMES, 0) {
			public boolean isCellEditable(int row, int column) {
				return false;
			}
		};
		derby = conn;
		DrawGUI();
		DefineButtons();
		SetButtonStates(false);
	}
	
	private void DrawGUI() {
		// Initialize UI classes
		arffonly = new FileNameExtensionFilter("Predictions","arff");
		ttable = new JTable(targetModel);
		tcontainer = new JScrollPane(ttable);
		tsave = new JButton("Create");
		sload = new JButton("Load");
		newDB = new JButton("Change Database");
		theader = new JButton("Edit Header");
		clear = new JButton("Clear Predictions");
		posValue = new JButton("Set Positive");
		negValue = new JButton("Set Negative");
		files = new JPanel();
		values = new JPanel();
		slabel = new JLabel("Source:");
		tlabel = new JLabel("Target:");
		sname = new JTextField("",20);
		sname.setEditable(false);
		tname = new JTextField("",20);
		tname.setEditable(false);
		
		// Begin drawing and layout manager assignment
		setBorder(new EmptyBorder(10, 5, 5, 10));
		setLayout(new BorderLayout());
		files.setLayout(new BoxLayout(files,BoxLayout.X_AXIS));
		values.setLayout(new BoxLayout(values,BoxLayout.X_AXIS));
		files.add(tlabel);
		files.add(tname);
		files.add(tsave);
		files.add(Box.createHorizontalGlue());
		files.add(slabel);
		files.add(sname);
		files.add(sload);
		files.add(Box.createHorizontalGlue());
		files.add(newDB);
		values.add(Box.createHorizontalGlue());
		values.add(theader);
		values.add(posValue);
		values.add(negValue);
		values.add(clear);
		values.add(Box.createHorizontalGlue());
		add(files,BorderLayout.NORTH);
		add(tcontainer,BorderLayout.CENTER);
		add(values,BorderLayout.SOUTH);
	}
	
	private void SetButtonStates(boolean state) {
		clear.setEnabled(state);
		theader.setEnabled(state);
		posValue.setEnabled(state);
		negValue.setEnabled(state);
	}
	
	private void DefineButtons() {
		sload.addActionListener(
			new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					source = new ARFF(loadfile());
					// TODO: Some sort of check to make sure ARFF processed correctly.
					try {
						derby.CreateSubtable(source.getItems(),sname.getText().substring(0, sname.getText().indexOf(".")) + "ARFF");
						clear.setEnabled(true);
					} catch (SQLException e1) {
						JOptionPane.showMessageDialog(null,"Error creating subtable.\n\nPlease contact administrator.","Database Error.",JOptionPane.WARNING_MESSAGE);
					}
				}
			}
		);
		
		tsave.addActionListener(
			new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					try {
						if (tsave.getText() == "Create") {
							if (createPrediction()) {
								tsave.setText("Save");
								tname.setText(tfile.getName());
								target = new ARFF();
								SetButtonStates(true);
							}	
						} else if (tsave.getText() == "Save") {
							target.clearItems();
							for (int i=0;i<targetModel.getRowCount();i++) {
								target.add(targetModel.getValueAt(i,1).toString(), targetModel.getValueAt(i,0).toString());
							}
							saveFile(target.getString(),tfile);
							//TODO: Save to file
							//TODO: Set modified to false
						}
					} catch (IOException ioe) {
						JOptionPane.showMessageDialog(null, "Error saving prediction. Ensure file exists and is not in use by another application.","Save Error",JOptionPane.ERROR_MESSAGE);
					}
				}
			}
		);
	
		clear.addActionListener(
			new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					if (sname.getText().length() > 0) {
						try {
							derby.Command("DROP TABLE " + sname.getText().substring(0,sname.getText().indexOf(".")) + "ARFF");
							derby.Command("DROP TABLE PREDICTION");
							sname.setText(null);
						} catch (SQLException e1) {
							JOptionPane.showMessageDialog(null, "Predictions already dropped from database","Drop Error",JOptionPane.WARNING_MESSAGE);
						}
					}
					if (tname.getText().length() > 0) {
						tname.setText(null);
						targetModel.setRowCount(0);
						tsave.setText("Create");
					}
					SetButtonStates(false);
				}
			}
		);
		
		posValue.addActionListener(
			new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					int selection = ttable.getSelectionModel().getSelectionMode();
					if (selection == ListSelectionModel.SINGLE_SELECTION) {
						targetModel.setValueAt("1.0",ttable.getSelectedRow(),0);
					} else {
						int[] selected = ttable.getSelectedRows();
						for(int i=0;i<selected.length;i++){
							targetModel.setValueAt("1.0",selected[i],0);
						}
					}
				}
			}
		);
		
		negValue.addActionListener(
				new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						int selection = ttable.getSelectionModel().getSelectionMode();
						if (selection == ListSelectionModel.SINGLE_SELECTION) {
							int selected = ttable.getSelectedRow();
							if (selected > 0) {
								targetModel.setValueAt("0",selected,0);
							}
						} else {
							int[] selected = ttable.getSelectedRows();
							for(int i=0;i<selected.length;i++){
								targetModel.setValueAt("0",selected[i],0);
							}
						}
					}
				}
			);
		
	}
	
	private String[] loadfile() {
		// TODO: Warning if target prediction has been modified but not saved?
		
		ArrayList<String> rawtext = new ArrayList<String>();
		String line;
		JFileChooser fdialog = new JFileChooser("./");
		fdialog.setFileFilter(arffonly);
		fdialog.showOpenDialog(this);
		File arffin = fdialog.getSelectedFile();
		sname.setText(arffin.getName());
		try {
			BufferedReader lines = new BufferedReader(new FileReader(arffin));
			while((line = lines.readLine()) != null){
				rawtext.add(line.trim());
			}
			lines.close();			
		} catch (FileNotFoundException e) {
			JOptionPane.showMessageDialog(null, "File not found. Please try again.","Loading Error",JOptionPane.ERROR_MESSAGE);
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Problem reading file. Please try again.","Loading Error",JOptionPane.ERROR_MESSAGE);
		} catch (NullPointerException e) {
			// TODO: Should anything happen if no file is selected?
		}

		//TODO: Update source textbox to show the name of the prediction file
		return rawtext.toArray(new String[rawtext.size()]);
	}
	
	private void saveFile(String[] contents, File savefile) throws IOException {
		BufferedWriter output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(savefile),"UTF8"));
		output.write("");
		for (int i=0;i<contents.length;i++){
			output.append(contents[i] + "\n");
		}
		output.close();
	}
	
	private boolean createPrediction() throws IOException {
		target = new ARFF();
		JFileChooser fdialog = new JFileChooser("./");
		fdialog.showSaveDialog(this);
		tfile = fdialog.getSelectedFile();
		while (tfile.exists()){
			int response = JOptionPane.showConfirmDialog(null,"Target filename already exists. Overwrite?","File exists",JOptionPane.YES_NO_OPTION);
			if (response == JOptionPane.YES_OPTION){
				return true;
			}
			else {
				fdialog.showSaveDialog(this);
				tfile = fdialog.getSelectedFile();
			}
		}
		tfile.createNewFile();
		return true;
	}
}
