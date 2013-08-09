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
import backend.*;

public class PredictionManager extends JPanel {
	PredictionTableModel targetModel;
	private Preferences prefs;
	private DerbyDB derby;
	private ARFF source,target;
	private JPanel filesPanel, buttonsPanel;
	private JScrollPane targetScroll;
	private JTable targetTable;
	private JTextField sourceName,targetName;
	private JButton targetSave,sourceLoad,startMapper,remove,setMatch,setMiss,targetHeader,targetRange,clear,loadFromSource;
	private JLabel sourceLabel,targetLabel;
	private Boolean modified,loaded;
	private File targetFile;
	private FileNameExtensionFilter arffOnly;
	private HeaderEdit headerEditor;
	private RangeEdit rangeEditor;
	private String volumeDataDir;
	//TODO: Have this passed in via Preferences (need it for genrecodes.ini anyway)
	
	public PredictionManager(DerbyDB conn, Preferences p) {
		prefs = p;
		targetModel = new PredictionTableModel();
		derby = conn;
		drawGUI();
		defineListeners();
		setButtonStates(false);
		modified = false;
		volumeDataDir = null;
		loaded = false;
		target = null;
	}
	
	private void drawGUI() {
		// Initialize & Configure UI classes
		arffOnly = new FileNameExtensionFilter("Predictions","arff");
		targetTable = new JTable(targetModel);
		targetTable.setAutoCreateColumnsFromModel(false);
		targetTable.setAutoResizeMode(JTable.AUTO_RESIZE_NEXT_COLUMN);
		targetTable.getColumnModel().getColumn(0).setPreferredWidth(200);
		targetTable.getColumnModel().getColumn(1).setPreferredWidth(200);
		targetTable.getColumnModel().getColumn(2).setPreferredWidth(300);
		targetTable.getColumnModel().getColumn(3).setPreferredWidth(40);
		targetTable.getColumnModel().getColumn(3).setMinWidth(40);
		targetTable.getColumnModel().getColumn(4).setPreferredWidth(60);
		targetTable.getColumnModel().getColumn(4).setMinWidth(60);
		targetTable.getColumnModel().getColumn(5).setPreferredWidth(60);
		targetTable.getColumnModel().getColumn(5).setMinWidth(60);
		targetTable.getColumnModel().getColumn(6).setPreferredWidth(60);
		targetTable.getColumnModel().getColumn(6).setMinWidth(60);
		targetTable.getColumnModel().getColumn(7).setPreferredWidth(60);
		targetTable.getColumnModel().getColumn(7).setMinWidth(60);
		targetTable.getColumnModel().getColumn(8).setPreferredWidth(60);
		targetTable.getColumnModel().getColumn(8).setMinWidth(60);
		targetScroll = new JScrollPane(targetTable);
		targetScroll.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);
		targetSave = new JButton("Create");
		sourceLoad = new JButton("Load");
		startMapper = new JButton("Page Mapper");
		remove = new JButton("Remove");
		targetHeader = new JButton("Edit Header");
		targetRange = new JButton("Edit Range");
		clear = new JButton("Clear Records");
		setMatch = new JButton("Set Match");
		setMiss = new JButton("Set Miss");
		loadFromSource = new JButton("Load Source Records");
		filesPanel = new JPanel();
		buttonsPanel = new JPanel();
		sourceLabel = new JLabel("Source:");
		targetLabel = new JLabel("Target:");
		sourceName = new JTextField("",20);
		sourceName.setEditable(false);
		targetName = new JTextField("",20);
		targetName.setEditable(false);
		
		// Begin panel and layout manager assignment
		setBorder(new EmptyBorder(10, 5, 5, 10));
		setLayout(new BorderLayout());
		filesPanel.setLayout(new BoxLayout(filesPanel,BoxLayout.X_AXIS));
		buttonsPanel.setLayout(new BoxLayout(buttonsPanel,BoxLayout.X_AXIS));
		filesPanel.add(targetLabel);
		filesPanel.add(targetName);
		filesPanel.add(targetSave);
		filesPanel.add(Box.createHorizontalGlue());
		filesPanel.add(sourceLabel);
		filesPanel.add(sourceName);
		filesPanel.add(sourceLoad);
		filesPanel.add(Box.createHorizontalGlue());
		filesPanel.add(startMapper);
		buttonsPanel.add(Box.createHorizontalGlue());
		buttonsPanel.add(remove);
		buttonsPanel.add(targetHeader);
		buttonsPanel.add(targetRange);
		buttonsPanel.add(setMatch);
		buttonsPanel.add(setMiss);
		buttonsPanel.add(clear);
		buttonsPanel.add(loadFromSource);
		buttonsPanel.add(Box.createHorizontalGlue());
		add(filesPanel,BorderLayout.NORTH);
		add(targetScroll,BorderLayout.CENTER);
		add(buttonsPanel,BorderLayout.SOUTH);
	}
	
	private void setButtonStates(boolean state) {
		/**
		 * A quick way to enable/disable all prediction manipulation buttons.
		 */
		remove.setEnabled(state);
		clear.setEnabled(state);
		targetHeader.setEnabled(state);
		targetRange.setEnabled(state);
		setMatch.setEnabled(state);
		setMiss.setEnabled(state);
		loadFromSource.setEnabled(state);
		startMapper.setEnabled(state);
	}
	
	private void defineListeners() {
		
		// *****BUTTONS THAT APPEAR IN THE TOP PANEL*****
		sourceLoad.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(loaded) {
					int response = JOptionPane.showConfirmDialog(null,"A source prediction has already been loaded.  Do you want to\nclear it from memory and load a different one?","Source Already Loaded",JOptionPane.YES_NO_OPTION);
					if(response == JOptionPane.YES_OPTION) {
						try {
							derby.command("DROP TABLE " + sourceName.getText().substring(0,sourceName.getText().indexOf(".")) + "ARFF");
							derby.command("DROP TABLE PREDICTION");
							sourceName.setText(null);
							loaded = false;
						} catch (SQLException e1) {
							JOptionPane.showMessageDialog(null, "Predictions already dropped from database","Derby Error",JOptionPane.WARNING_MESSAGE);
						}
					} else {
						return;
					}
				}
				String input[] = loadfile();
				if (input == null) {
					return;
				}
				source = new ARFF(input);
				// TODO: Some sort of check to make sure ARFF processed correctly.
				try {
					derby.createSubtable(source.getItems(),sourceName.getText().substring(0, sourceName.getText().indexOf(".")) + "ARFF");
					clear.setEnabled(true);
					loadFromSource.setEnabled(true);
					loaded = true;
				} catch (SQLException e1) {
					JOptionPane.showMessageDialog(null,"Error creating subtable.\n\nPlease contact administrator.","Database Error.",JOptionPane.WARNING_MESSAGE);
				}
			}
		});
		
		targetSave.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					if (targetSave.getText() == "Create") {
						if (createPrediction()) {
							targetSave.setText("Save");
							targetName.setText(targetFile.getName());
							target = new ARFF();
							setButtonStates(true);
							if(!loaded){
								loadFromSource.setEnabled(false);
							}
						}	
					} else if (modified) {
						addToARFF();
						saveFile(target.getString(),targetFile);
						modified = false;
						targetSave.setText("Save");
						JOptionPane.showMessageDialog(null, "Prediction saved successfully to " + targetFile.getName(),"Save Successful",JOptionPane.INFORMATION_MESSAGE);
					}
				} catch (IOException ioe) {
					JOptionPane.showMessageDialog(null, "Error saving prediction. Ensure file exists and is not in use by another application.","Save Error",JOptionPane.ERROR_MESSAGE);
				}
			}
		});
		
		startMapper.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int selected[] = targetTable.getSelectedRows();
				if(selected.length > 1) {
					JOptionPane.showMessageDialog(null, "Page Mapper can only accept one volume at a time.","Invalid Selection",JOptionPane.ERROR_MESSAGE);
					return;
				} else if (selected.length < 1) {
					return;
				}
				else if(!targetModel.isMapping()) {
					JOptionPane.showMessageDialog(null, "Please identify where volume data is stored.  Your choice will be saved for this session only.","Session Initalization",JOptionPane.OK_OPTION);
					JFileChooser vdchoose = new JFileChooser(System.getProperty("user.dir"));
					vdchoose.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
					vdchoose.showOpenDialog(null);
					volumeDataDir = vdchoose.getSelectedFile().getAbsolutePath() + "/";
					vdchoose = null;
					if(!prefs.hasGenreCodes()) {
						JOptionPane.showMessageDialog(null, "No genre codes table selected.  Please locate the file containing your genre codes.\nYour choice will be stored for future sessions.","Session Initalization",JOptionPane.OK_OPTION);
						JFileChooser codechoose = new JFileChooser(System.getProperty("user.dir"));
						codechoose.setFileFilter(new FileNameExtensionFilter("Configuration files","ini"));
						codechoose.showOpenDialog(null);
						prefs.setGenreCodes(codechoose.getSelectedFile().getAbsolutePath());
					}
				}
				try {
					VolumeReader volume = new VolumeReader(targetModel.getValueAt(selected[0],PredictionTableModel.HTID_COL).toString(),volumeDataDir,false);
					//TODO: Pass in pageMapDir from Preferences!
					PageMapper pagemap = new PageMapper(volume,prefs);
					if(pagemap.complete) {
						targetModel.volumeMapped(selected[0]);
					}
				} catch (FileNotFoundException e1) {
					int choice = JOptionPane.showConfirmDialog(null, "Selected Volume does not exist in data directory. Reset data directory?","Volume Not Found",JOptionPane.YES_NO_OPTION);
					if (choice == JOptionPane.YES_OPTION) {
						targetModel.setMapping(false);
					}
					return;
				}
				
			}
		});
		
		// *****BUTTONS THAT APPEAR IN THE BOTTOM PANEL*****
		remove.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (targetTable.getSelectedRowCount() != 0) {
					int selected[] = targetTable.getSelectedRows();
					for(int i=selected.length-1;i>=0;i--) {
						targetModel.removeRow(selected[i]);
					}
				}
			}
		});
	
		clear.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (sourceName.getText().length() > 0) {
					try {
						derby.dropTables();
						sourceName.setText(null);
					} catch (SQLException e1) {
						JOptionPane.showMessageDialog(null, "Predictions already dropped from database","Derby Error",JOptionPane.WARNING_MESSAGE);
					}
				}
				if (targetName.getText().length() > 0) {
					targetName.setText(null);
					targetSave.setText("Create");
				}
				targetModel.setRowCount(0);
				setButtonStates(false);
				modified = false;
				loaded = false;
			}
		});
		
		setMatch.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int[] selected = targetTable.getSelectedRows();
				for(int i=0;i<selected.length;i++){
					targetModel.setValueAt("1.0",selected[i],PredictionTableModel.PROBABILITY_COL);
				}
			}
		});
		
		setMiss.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int[] selected = targetTable.getSelectedRows();
				for(int i=0;i<selected.length;i++){
					targetModel.setValueAt("0",selected[i],PredictionTableModel.PROBABILITY_COL);
				}
			}
		});
		
		targetHeader.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if (target == null) {
					JOptionPane.showMessageDialog(null, "You must create a prediction to save to before you can edit the header.","Target Missing",JOptionPane.ERROR_MESSAGE);
					return;
				}
				headerEditor = new HeaderEdit();
				headerEditor.setHeading(target.getHeader());
				headerEditor.setRelation(target.getRelation());
				headerEditor.setVisible(true);
				if (headerEditor.getResult()) {
					target.setHeader(headerEditor.getHeading());
					target.setRelation(headerEditor.getRelation());
					targetSave.setText("Save*");
					modified = true;
				}
			}
		});
		
		targetRange.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int[] selected = targetTable.getSelectedRows();
				if (selected.length == 1) {
					rangeEditor = new RangeEdit();
					rangeEditor.setRange(targetModel.getRange(selected[0]));
					rangeEditor.setVisible(true);
					if(rangeEditor.getResult()) {
						targetModel.setRange(selected[0],rangeEditor.getRange());
					}
				} else {
					JOptionPane.showMessageDialog(null, "Can only view one record at a time.","Selection Error",JOptionPane.WARNING_MESSAGE);
				}
				
				
			}
		});
		
		loadFromSource.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				loadSourceRecords();
			}
		});
		
		// ***** DATA MODEL LISTENER *****
		targetModel.addTableModelListener(new TableModelListener() {
			public void tableChanged(TableModelEvent e) {
				if (targetSave.getText() != "Create") {
					targetSave.setText("Save*");
				} else {
					targetHeader.setEnabled(false);
				}
				if (targetModel.getRowCount() != 0 && !modified) {
					modified = true;
					setButtonStates(true);
					if (!loaded) {
						loadFromSource.setEnabled(false);
					}
					// Check to see if the last row has a pagemap (so new additions will get marked).
					String latestHTid = targetModel.getValueAt(targetModel.getRowCount()-1,PredictionTableModel.HTID_COL).toString();
					if(checkForMap(latestHTid)) {
						targetModel.volumeMapped(targetModel.getRowCount()-1);
					}
				} else if (targetModel.getRowCount() == 0) {
					modified = false;
					setButtonStates(false);
					if (loaded) {
						loadFromSource.setEnabled(true);
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
		JFileChooser fdialog = new JFileChooser(System.getProperty("user.dir"));
		fdialog.setFileFilter(arffOnly);
		int result = fdialog.showOpenDialog(this);
		if (result != JFileChooser.APPROVE_OPTION) {
			return null;
		}
		File arffin = fdialog.getSelectedFile();
		sourceName.setText(arffin.getName());
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
		JFileChooser fdialog = new JFileChooser(System.getProperty("user.dir"));
		fdialog.showSaveDialog(this);
		targetFile = fdialog.getSelectedFile();
		while (targetFile.exists()){
			int response = JOptionPane.showConfirmDialog(null,"Target filename already exists. Overwrite?","File exists",JOptionPane.YES_NO_OPTION);
			if (response == JOptionPane.YES_OPTION){
				return true;
			}
			else {
				fdialog.showSaveDialog(this);
				targetFile = fdialog.getSelectedFile();
			}
		}
		targetFile.createNewFile();
		return true;
	}
	
	private void addToARFF() {
		/**
		 * Transfers items from the target table model to the prediction data structure. It's quicker to erase all items and copy the entire table than check to see which items have been added or removed.
		 */
		target.clearItems();
		for (int i=0;i<targetModel.getRowCount();i++) {
			String[] record = targetModel.getRow(i);
			target.add(record[PredictionTableModel.HTID_COL],record[PredictionTableModel.PAGESTART_COL],record[PredictionTableModel.PAGEEND_COL],record[PredictionTableModel.PARTSTART_COL],record[PredictionTableModel.PARTEND_COL],record[PredictionTableModel.PROBABILITY_COL]);
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
						targetModel.addPrediction(csv[0],records[recindex][1],records[recindex][2],records[recindex][3],csv[1],csv[2],csv[3],csv[4],csv[5]);
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
		if(target==null) {
			JOptionPane.showMessageDialog(null, "Please create a target prediction file to save to.","Target Missing.",JOptionPane.WARNING_MESSAGE);
			return false;
		}
		
		try {
			addToARFF();
			saveFile(target.getString(),targetFile);
			return true;
		} catch (IOException e) {
			JOptionPane.showMessageDialog(null, "Error saving prediction. Ensure file exists and is not in use by another application.","Save Error",JOptionPane.ERROR_MESSAGE);
			return false;
		}
	}
	
	public boolean checkForMap(String htid) {
		VolumeReader checker = new VolumeReader();
		checker.learnNameParts(htid);
		if(new File(prefs.getMapDir() + checker.getFileID() + ".tsv").exists()) {
			return true;
		} else {
			return false;
		}
	}
}
