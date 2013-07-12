package gui;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.sql.SQLException;
import java.util.ArrayList;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.event.TableModelEvent;
import javax.swing.event.TableModelListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;
import backend.ARFF;
import backend.DerbyDB;
import backend.PredictionTableModel;

public class PredictionManager extends JPanel {
	PredictionTableModel tmodel;
	private DerbyDB derby;
	private ARFF source,target;
	private JPanel files, values;
	private JScrollPane tcontainer;
	private JTable ttable;
	private JTextField sname,tname;
	private JButton tsave,sload,newDB,remove,posValue,negValue,theader,clear,allfromsource;
	private JLabel slabel,tlabel;
	private Boolean modified,loaded;
	private File tfile;
	private FileNameExtensionFilter arffonly;
	private HeaderEdit heditor;
	
	public PredictionManager(DerbyDB conn) {
		// Override default settings in table model to forbid users from editing cells because Java doesn't provide this option natively for some reason
		tmodel = new PredictionTableModel();
		derby = conn;
		drawGUI();
		defineListeners();
		setButtonStates(false);
		modified = false;
		loaded = false;
	}
	
	private void drawGUI() {
		// Initialize & Configure UI classes
		arffonly = new FileNameExtensionFilter("Predictions","arff");
		ttable = new JTable(tmodel);
		ttable.setAutoCreateColumnsFromModel(false);
		ttable.setAutoResizeMode(JTable.AUTO_RESIZE_NEXT_COLUMN);
		ttable.getColumnModel().getColumn(0).setPreferredWidth(200);
		ttable.getColumnModel().getColumn(1).setPreferredWidth(200);
		ttable.getColumnModel().getColumn(2).setPreferredWidth(300);
		ttable.getColumnModel().getColumn(3).setPreferredWidth(40);
		ttable.getColumnModel().getColumn(3).setMinWidth(40);
		ttable.getColumnModel().getColumn(4).setPreferredWidth(60);
		ttable.getColumnModel().getColumn(4).setMinWidth(60);
		ttable.getColumnModel().getColumn(5).setPreferredWidth(60);
		ttable.getColumnModel().getColumn(5).setMinWidth(60);
		ttable.getColumnModel().getColumn(6).setPreferredWidth(60);
		ttable.getColumnModel().getColumn(6).setMinWidth(60);
		ttable.getColumnModel().getColumn(7).setPreferredWidth(60);
		ttable.getColumnModel().getColumn(7).setMinWidth(60);
		ttable.getColumnModel().getColumn(8).setPreferredWidth(60);
		ttable.getColumnModel().getColumn(8).setMinWidth(60);
		tcontainer = new JScrollPane(ttable);
		tcontainer.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
		tsave = new JButton("Create");
		sload = new JButton("Load");
		newDB = new JButton("Change Database");
		remove = new JButton("Remove");
		theader = new JButton("Edit Header");
		clear = new JButton("Clear Predictions");
		posValue = new JButton("Set Positive");
		negValue = new JButton("Set Negative");
		allfromsource = new JButton("Load Source Records");
		files = new JPanel();
		values = new JPanel();
		slabel = new JLabel("Source:");
		tlabel = new JLabel("Target:");
		sname = new JTextField("",20);
		sname.setEditable(false);
		tname = new JTextField("",20);
		tname.setEditable(false);
		
		// Begin panel and layout manager assignment
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
		values.add(remove);
		values.add(theader);
		values.add(posValue);
		values.add(negValue);
		values.add(clear);
		values.add(allfromsource);
		values.add(Box.createHorizontalGlue());
		add(files,BorderLayout.NORTH);
		add(tcontainer,BorderLayout.CENTER);
		add(values,BorderLayout.SOUTH);
	}
	
	private void setButtonStates(boolean state) {
		/**
		 * A quick way to enable/disable all prediction manipulation buttons.
		 */
		remove.setEnabled(state);
		clear.setEnabled(state);
		theader.setEnabled(state);
		posValue.setEnabled(state);
		negValue.setEnabled(state);
		allfromsource.setEnabled(state);
	}
	
	private void defineListeners() {
		sload.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(loaded) {
					int response = JOptionPane.showConfirmDialog(null,"A source prediction has already been loaded.  Do you want to\nclear it from memory and load a different one?","Source Already Loaded",JOptionPane.YES_NO_OPTION);
					if(response == JOptionPane.YES_OPTION) {
						try {
							derby.command("DROP TABLE " + sname.getText().substring(0,sname.getText().indexOf(".")) + "ARFF");
							derby.command("DROP TABLE PREDICTION");
							sname.setText(null);
							loaded = false;
						} catch (SQLException e1) {
							JOptionPane.showMessageDialog(null, "Predictions already dropped from database","Derby Error",JOptionPane.WARNING_MESSAGE);
						}
					} else {
						return;
					}
				}
				source = new ARFF(loadfile());
				// TODO: Some sort of check to make sure ARFF processed correctly.
				try {
					derby.createSubtable(source.getItems(),sname.getText().substring(0, sname.getText().indexOf(".")) + "ARFF");
					clear.setEnabled(true);
					allfromsource.setEnabled(true);
					loaded = true;
				} catch (SQLException e1) {
					JOptionPane.showMessageDialog(null,"Error creating subtable.\n\nPlease contact administrator.","Database Error.",JOptionPane.WARNING_MESSAGE);
				}
			}
		});
		
		tsave.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					if (tsave.getText() == "Create") {
						if (createPrediction()) {
							tsave.setText("Save");
							tname.setText(tfile.getName());
							target = new ARFF();
							setButtonStates(true);
							if(!loaded){
								allfromsource.setEnabled(false);
							}
						}	
					} else if (modified) {
						addToARFF();
						saveFile(target.getString(),tfile);
						modified = false;
						tsave.setText("Save");
						JOptionPane.showMessageDialog(null, "Prediction saved successfully to " + tfile.getName(),"Save Successful",JOptionPane.INFORMATION_MESSAGE);
					}
				} catch (IOException ioe) {
					JOptionPane.showMessageDialog(null, "Error saving prediction. Ensure file exists and is not in use by another application.","Save Error",JOptionPane.ERROR_MESSAGE);
				}
			}
		});
		
		remove.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (ttable.getSelectedRowCount() != 0) {
					int selected[] = ttable.getSelectedRows();
					for(int i=selected.length-1;i>=0;i--) {
						tmodel.removeRow(selected[i]);
					}
				}
			}
		});
	
		clear.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (sname.getText().length() > 0) {
					try {
						derby.dropTables();
						sname.setText(null);
					} catch (SQLException e1) {
						JOptionPane.showMessageDialog(null, "Predictions already dropped from database","Derby Error",JOptionPane.WARNING_MESSAGE);
					}
				}
				if (tname.getText().length() > 0) {
					tname.setText(null);
					tsave.setText("Create");
				}
				tmodel.setRowCount(0);
				setButtonStates(false);
				modified = false;
				loaded = false;
			}
		});
		
		posValue.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int selection = ttable.getSelectionModel().getSelectionMode();
				if (selection == ListSelectionModel.SINGLE_SELECTION) {
					tmodel.setValueAt("1.0",ttable.getSelectedRow(),0);
				} else {
					int[] selected = ttable.getSelectedRows();
					for(int i=0;i<selected.length;i++){
						tmodel.setValueAt("1.0",selected[i],0);
					}
				}
			}
		});
		
		negValue.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int selection = ttable.getSelectionModel().getSelectionMode();
				if (selection == ListSelectionModel.SINGLE_SELECTION) {
					int selected = ttable.getSelectedRow();
					if (selected > 0) {
						tmodel.setValueAt("0",selected,0);
					}
				} else {
					int[] selected = ttable.getSelectedRows();
					for(int i=0;i<selected.length;i++){
						tmodel.setValueAt("0",selected[i],0);
					}
				}
			}
		});
		
		theader.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				heditor = new HeaderEdit();
				heditor.setHeading(target.getHeader());
				heditor.setRelation(target.getRelation());
				heditor.setVisible(true);
				if (heditor.getResult()) {
					target.setHeader(heditor.getHeading());
					target.setRelation(heditor.getRelation());
					tsave.setText("Save*");
					modified = true;
				}
			}
		});
		
		allfromsource.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				loadSourceRecords();
			}
		});
		
		tmodel.addTableModelListener(new TableModelListener() {
			public void tableChanged(TableModelEvent e) {
				if (tsave.getText() != "Create") {
					tsave.setText("Save*");
				}
				if (tmodel.getRowCount() != 0 && !modified) {
					modified = true;
					setButtonStates(true);
					if (!loaded) {
						allfromsource.setEnabled(false);
					}
				} else if (tmodel.getRowCount() == 0) {
					modified = false;
					setButtonStates(false);
					if (loaded) {
						allfromsource.setEnabled(true);
						clear.setEnabled(true);
					}
				}
			}
		});
		
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
		return rawtext.toArray(new String[rawtext.size()]);
	}
	
	private void saveFile(String[] contents, File savefile) throws IOException {
		BufferedWriter output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(savefile),"UTF-8"));
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
	
	private void addToARFF() {
		/**
		 * Transfers items from the target table model to the prediction data structure. It's quicker to erase all items and copy the entire table than check to see which items have been added or removed.
		 */
		target.clearItems();
		for (int i=0;i<tmodel.getRowCount();i++) {
			target.add(tmodel.getValueAt(i,1).toString(), tmodel.getValueAt(i,0).toString());
		}
	}
	
	private void loadSourceRecords() {
		/**
		 * Checks the source prediction's internal csv against it's corresponding subtable in the Derby database. All found items are stored in the target table model, and all missing items are reported.
		 */
		try {
			String[][] records = derby.query("SELECT HTID, TITLE, AUTHOR, DATE FROM PREDICTION");			
			String[] arff = source.getString();
			String notfound = "";
			for(int i=0;i<arff.length;i++) {
				if(!arff[i].startsWith("%") && !arff[i].startsWith("@")) {
					String[] csv = arff[i].split(",");
					int recindex = findIndex(csv[0],records);
					if (recindex > -1) {
						tmodel.addPrediction(csv[0],records[recindex][1],records[recindex][2],records[recindex][3],csv[1],csv[2],csv[3],csv[4],csv[5]);
					} else {
						notfound += "\n" + csv[0]; 
					}
				} 
			}
			if (notfound != "") {
				JOptionPane.showMessageDialog(null, "The following predictions were not found in the database:" + notfound,"Predictions Not Found",JOptionPane.WARNING_MESSAGE);
			}
			
		} catch (SQLException e) {
			JOptionPane.showMessageDialog(null, "This database query could not be executed. Please consult derby.log.","Derby Error",JOptionPane.ERROR_MESSAGE);
		}		
	}
	
	private int findIndex(String htid, String[][] records) {
		/**
		 * A simple check that returns the index of the record array that contains an HTid matching the one passed into the method.
		 */
		int index = -1;
		for(int i=0;i<records.length;i++) {
			if(htid.equals(records[i][0])) {
				return i;
			}
		}
		return index;
	}
	
	public boolean getSaveState() {
		/**
		 * This method allows other classes to check whether the target prediction data has been saved since it was modified.  For use with doSave and window listeners in containing classes.
		 */
		return modified;
	}
	
	public boolean doSave() {
		/**
		 * This method allows other classes to instruct this class to perform save operations.  Useful for window listeners in containing classes that prompt users to save before closing the program. 
		 */
		try {
			addToARFF();
			saveFile(target.getString(),tfile);
			return true;
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Error saving prediction. Ensure file exists and is not in use by another application.","Save Error",JOptionPane.ERROR_MESSAGE);
			return false;
		}
	}
}
