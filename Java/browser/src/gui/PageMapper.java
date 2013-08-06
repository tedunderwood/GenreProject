package debug;

import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Set;
import java.util.TreeMap;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;

import backend.VolumeReader;

public class PageMapper extends JFrame {
	private JPanel pagePanel,actionsPanel,movePanel,centerPanel,savePanel,storedPanel;
	private JLabel position,storedCount;
	private JTable storedTable;
	private JTextArea pagetextArea;
	private JTextField scanNumField,skipNumField;
	private JButton store,scan,save,load,cancel,skip;
	private JScrollPane pageScroll,storedScroll;
	private JCheckBox reverse;
	private DefaultTableModel storedModel;
	private VolumeReader volume;
	private int current;
	private JComboBox<String> codeBox;
	private TreeMap<Integer,String> codeDictionary;
	private TreeMap<Integer,Double> capsDictionary;
	private final double threshold = 2.25;
	private File mapFile;
	
	//TEMPORARY CODEREADERFILES
	private String[][] generalCodes, pageCodes;
	private String codesini = "genrecodes.ini";
	
	public PageMapper (VolumeReader input) {
		volume = input;
		current = 0;
		codeDictionary = new TreeMap<Integer,String>();
		capsDictionary = new TreeMap<Integer,Double>();
		storedModel = new DefaultTableModel();
		codeReader(codesini);
		drawGUI();
		buildCodeBox();
		displayPage(volume.getPage(current));
		defineListeners();
	}
	
	private void drawGUI() {
		Dimension buttonSize = new Dimension(100,30);
		Dimension textSize = new Dimension(100,30);
		Dimension storedSize = new Dimension(200,100);
		GridBagConstraints buttonProperties = new GridBagConstraints();
		buttonProperties.gridx = 0;
		GridBagConstraints textProperties = new GridBagConstraints();
		buttonProperties.gridx = 1;
		
		setSize(600,700);
		setLayout(new BorderLayout());
		pagePanel = new JPanel();
		pagePanel.setLayout(new BorderLayout());
		pagePanel.setBorder(new EmptyBorder(10, 10, 5, 10));
		pagePanel.setPreferredSize(new Dimension(600,500));
		actionsPanel = new JPanel();
		actionsPanel.setLayout(new BorderLayout());
		actionsPanel.setBorder(new EmptyBorder(5, 10, 10, 10));
		actionsPanel.setPreferredSize(new Dimension(600,200));
		movePanel = new JPanel();
		movePanel.setLayout(new GridBagLayout());
		movePanel.setMaximumSize(new Dimension(225,150));
		centerPanel = new JPanel();
		centerPanel.setLayout(new BoxLayout(centerPanel,BoxLayout.X_AXIS));
		savePanel = new JPanel();
		savePanel.setLayout(new BoxLayout(savePanel,BoxLayout.X_AXIS));
		storedPanel = new JPanel();
		storedPanel.setLayout(new BoxLayout(storedPanel,BoxLayout.Y_AXIS));
		
		position = new JLabel();
		pagetextArea = new JTextArea();
		pagetextArea.setEditable(false);
		pageScroll = new JScrollPane(pagetextArea);
		scanNumField = new JTextField();
		scanNumField.setPreferredSize(textSize);
		skipNumField = new JTextField();
		skipNumField.setPreferredSize(textSize);
		scan = new JButton("Scan To");
		scan.setPreferredSize(buttonSize);
		skip = new JButton("Skip To");
		skip.setPreferredSize(buttonSize);
		store = new JButton("Store Code");
		store.setPreferredSize(buttonSize);
		codeBox = new JComboBox<String>();
		reverse = new JCheckBox("Reverse");
		reverse.setSelected(false);
		reverse.setPreferredSize(textSize);
		save = new JButton("Save");
		save.setPreferredSize(buttonSize);
		load = new JButton("Load");
		load.setPreferredSize(buttonSize);
		cancel = new JButton("Cancel");
		cancel.setPreferredSize(buttonSize);
		storedTable = new JTable(storedModel);
		storedTable.setEnabled(false);
		storedScroll = new JScrollPane(storedTable);
		storedScroll.setPreferredSize(storedSize);
		storedScroll.setAlignmentX(LEFT_ALIGNMENT);
		storedCount = new JLabel("Stored: 0");
		storedCount.setAlignmentX(LEFT_ALIGNMENT);
		
		buttonProperties.gridy = 0;
		textProperties.gridy = 0;
		movePanel.add(store,buttonProperties);
		movePanel.add(reverse,textProperties);
		buttonProperties.gridy = 1;
		textProperties.gridy = 1;
		movePanel.add(scan,buttonProperties);
		movePanel.add(scanNumField,textProperties);
		buttonProperties.gridy = 2;
		textProperties.gridy = 2;
		movePanel.add(skip,buttonProperties);
		movePanel.add(skipNumField,textProperties);
		
		savePanel.add(Box.createHorizontalGlue());
		savePanel.add(save);
		savePanel.add(cancel);
		savePanel.add(Box.createHorizontalGlue());
		
		pagePanel.add(position,BorderLayout.NORTH);
		pagePanel.add(pageScroll,BorderLayout.CENTER);
		
		storedPanel.add(storedCount);
		storedPanel.add(storedScroll);
		
		centerPanel.add(Box.createHorizontalGlue());
		centerPanel.add(movePanel);
		centerPanel.add(Box.createHorizontalGlue());
		centerPanel.add(storedPanel);
		centerPanel.add(Box.createHorizontalGlue());
		
		actionsPanel.add(codeBox,BorderLayout.NORTH);
		actionsPanel.add(centerPanel,BorderLayout.CENTER);
		actionsPanel.add(savePanel,BorderLayout.SOUTH);
		
		add(pagePanel,BorderLayout.CENTER);
		add(actionsPanel,BorderLayout.SOUTH);
		setVisible(true);
	}
	
	private void displayPage(String[] lines) {
		String pageText = new String();
		for(int i=0;i<lines.length;i++){
			pageText += lines[i] + "\n";
		}
		pagetextArea.setText(pageText);
		pagetextArea.setCaretPosition(0);
		scanNumField.setText("");
		skipNumField.setText("");
		position.setText("Page " + Integer.toString(current) + " / " + Integer.toString(volume.getLength()-1));
	}
	
	int countCaps(String[] lines) {
		int index, caps = 0;
		for(int i=0;i<lines.length;i++){
			index = 0;
			if(!Character.isLetterOrDigit(lines[i].charAt(0))) {
				// In the event that the first character is a quotation mark, skip.
				index = 1;
			}
			if(Character.isUpperCase(lines[i].charAt(index))) {
				caps++;
			}
		}
		return caps;
	}
	
	private double getCapsPercent(String[] lines) {
		int index, linecount = 0, caps = 0;
		for(int i=0;i<lines.length;i++){
			if (lines[i].length() < 2) {
				continue;
			}
			linecount++;
			index = 0;
			if(!Character.isLetterOrDigit(lines[i].charAt(0))) {
				// In the event that the first character is a quotation mark, skip.
				index = 1;
			}
			if(Character.isUpperCase(lines[i].charAt(index))) {
				caps++;
			}
		}
		
		return (double)caps / linecount;
	}
	
	private double getMean() {
		/**
		 * Returns the mean of all stored first character capital percentages for stored 
		 * pages. Because pages that are too short are assigned -1.0, the total number of
		 * pages counted will not match the size of the dictionary.  Returns 0 to avoid
		 * division error if dictionary is empty.
		 */
		double sum = 0;
		int total = 0;
		storePagePercent(); // In case the current page is not stored, store it.
		Integer[] keys = getIterableKeys(capsDictionary.keySet());
		for(int i=0;i<keys.length;i++) {
			if(capsDictionary.get(keys[i]) != -1.0) {
				total++;
				sum+=capsDictionary.get(keys[i]);
			}
		}
		if (total==0){
			return 0.0;
		} else {
			return sum / total;
		}
	}
	
	double getStanDev() {
		/**
		 * Returns the standard deviation of all stored first character capital percentages
		 * for stored pages.  Because pages that are too short are assigned -1.0, the total
		 * number of pages counted will not match the size of dictionary.  Returns 0 to
		 * avoid division error if dictionary is empty.
		 */
		double variance = 0.0;
		int total = 0;
		storePagePercent(); // In case the current page is not stored, store it.
		Integer[] keys = getIterableKeys(capsDictionary.keySet());
		for(int i=0;i<keys.length;i++) {
			if(capsDictionary.get(keys[i]) != -1.0) {
				total++;
				variance+=Math.pow(capsDictionary.get(keys[i]) - getMean(),2);
			}
		}
		if(total==0) {
			return 0.0;
		} else {
			return Math.sqrt(variance/total);
		}
	}
	
	private void storePageData() {
		storePagePercent();
		storePageCode();
	}
	
	private void storePagePercent() {
		if(volume.getPage(current).length >= 3) {
			capsDictionary.put(current, getCapsPercent(volume.getPage(current)));
		} else {
			capsDictionary.put(current, -1.0);
		}
	}
	
	private void storePageCode() {
		codeDictionary.put(current,getCode());
		updateCodeDisplay();
		storedCount.setText("Stored: " + codeDictionary.size() + "/" + volume.getLength());
	}
	
	private void updateCodeDisplay() {
		/**
		 * This function builds an array from codeDictionary and sets it as data vector for scrollModel.
		 */
		String[][] codes = new String[codeDictionary.size()][2];
		String[] columns = {"Page","Code"};
		Integer[] keys = getIterableKeys(codeDictionary.keySet());
		for(int i=0;i<keys.length;i++) {
			codes[i][0] = keys[i].toString();
			codes[i][1] = codeDictionary.get(keys[i]);
		}
		storedModel.setDataVector(codes,columns);
	}
	
	private void defineListeners() {
		store.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(isValidCode()) {
					storePageData();
					if (!reverse.isSelected()) {
						if (current < volume.getLength()-1) {
							current++;
							displayPage(volume.getPage(current));
						} else {
							JOptionPane.showMessageDialog(null,"End of volume reached. Cannot advance further in current direction.","Traversal Error",JOptionPane.WARNING_MESSAGE);
						}
					} else {
						if (current > 0) {
							current--;
							displayPage(volume.getPage(current));
						} else {
							JOptionPane.showMessageDialog(null,"Start of volume reached. Cannot advance further in current direction.","Traversal Error",JOptionPane.WARNING_MESSAGE);
						}
					}
				} else {
					JOptionPane.showMessageDialog(null,"Invalid selection. Please choose a genre code.","Invalid Selection",JOptionPane.WARNING_MESSAGE);
				}
			}
		});
		
		scan.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(isValidCode()) {
					try {
						int increment;
						int toPage = Integer.parseInt(scanNumField.getText());
						if (toPage > current && toPage < volume.getLength()) {
							increment = 1;
						} else if (toPage < current) {
							increment = -1;
							reverse.setEnabled(true);
						} else if (toPage >= volume.getLength()) {
							increment = -1;
							reverse.setEnabled(true);
							toPage = (int)current;
							current = volume.getLength()-1;
						} else {
							JOptionPane.showMessageDialog(null, "Please enter a page number other than the current one.","Page Advance Error",JOptionPane.ERROR_MESSAGE);
							return;
						}
						
						for(int i=current;i!=toPage;i+=increment) {
							current = i;
							displayPage(volume.getPage(current));
							if(Math.abs(getCapsPercent(volume.getPage(current)) - getMean()) > getStanDev()*threshold) {
								int choice = JOptionPane.showConfirmDialog(null,"Are you sure you wish to assign " + getCode() + " to page " +Integer.toString(current) +"?","Threshold Reached",JOptionPane.YES_NO_OPTION);
								if(choice == JOptionPane.NO_OPTION) {
									return;
								}
							}
							storePageData();
						}
						if (current != 0 && current != volume.getLength()-1) {
							// If the end of the volume has not been reached, then show user the next page so they can decide on a code.
							current+=increment;
							displayPage(volume.getPage(current));
						}
							
					} catch (NumberFormatException badnum) {
						JOptionPane.showMessageDialog(null,"Enter a valid page number.","Invalid Selection",JOptionPane.ERROR_MESSAGE);
						return;
					}
				} else {
					JOptionPane.showMessageDialog(null,"Invalid selection. Please choose a genre code.","Invalid Selection",JOptionPane.ERROR_MESSAGE);
				}
			}
		});
		
		skip.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					int toPage = Integer.parseInt(skipNumField.getText());
					if (toPage < 0 || toPage >= volume.getLength()) {
						JOptionPane.showMessageDialog(null, "Specified page is not within range.","Invalid Selection",JOptionPane.ERROR_MESSAGE);
					} else {
						current = toPage;
						displayPage(volume.getPage(current));
					}
				} catch (NumberFormatException badnum) {
					JOptionPane.showMessageDialog(null,"Enter a valid page number.","Invalid Selection",JOptionPane.ERROR_MESSAGE);
					return;
				}
			}
		});
		
		save.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int missing = volume.getLength() - codeDictionary.size();
				if(missing > 0) {
					JOptionPane.showMessageDialog(null, "Page Map is missing " + Integer.toString(missing) + " codes.\nSkipping to first uncoded page.","Incomplete Map.",JOptionPane.WARNING_MESSAGE);
					for(int i=0;i<volume.getLength();i++) {
						if(!codeDictionary.containsKey(i)) {
							current = i;
							displayPage(volume.getPage(current));
							return;
						}
					}
				} else {
					doSave();
				}
			}
		});
	}
	
	private Integer[] getIterableKeys(Set<Integer> keys) {
		return keys.toArray(new Integer[keys.size()]);
	}
	
	private boolean isValidCode() {
		/**
		 * Checks to make sure that the user has not selected a category label. Returns true of the user has selected a genre code.
		 */
		if(codeBox.getSelectedIndex() == 0) {
			// The first item will always be a category label
			return false;
		} else if (codeBox.getSelectedIndex() == generalCodes.length + 1 || codeBox.getSelectedIndex() == generalCodes.length + 2) {
			// Because of the first label, the list is effectively 1-indexed.  So spacer and next label will be at length + 1, 2 respectively.
			return false;
		} else {
			// If none of the others hit, then it should be a valid code
			return true;
		}
	}
	
	private String getCode() {
		/**
		 * Calculates the index of the selected genre code label and returns the label as a String.
		 */
		int selected = codeBox.getSelectedIndex(); 
		if (selected <= generalCodes.length) {
			return generalCodes[selected-1][0];
		} else {
			return pageCodes[selected-(generalCodes.length+3)][0];
		}
	}
	
	private void buildCodeBox() {
		codeBox.addItem("GENERAL CODES");
		for (int i=0;i<generalCodes.length;i++) {
			codeBox.addItem(generalCodes[i][0] + " - " + generalCodes[i][1]);
		}
		codeBox.addItem(" ");
		codeBox.addItem("PAGE ONLY CODES");
		for (int i=0;i<pageCodes.length;i++) {
			codeBox.addItem(pageCodes[i][0] + " - " + pageCodes[i][1]);
		}
	}
	
	private void codeReader (String filename) {
		///TODO: Transfer to Preferences after prototype is functional
		String line;
		ArrayList<String[]> all, page;
		all = new ArrayList<String[]>();
		page = new ArrayList<String[]>();
		boolean both = true;
		try {
			InputStream codesIn = new FileInputStream(new File(filename));
			BufferedReader inLines = new BufferedReader(new InputStreamReader(codesIn,Charset.forName("UTF-8")));
			while ((line = inLines.readLine()) != null) {
				if (line.trim().length() > 0) {
					if(line.contains("#GENERAL")) {
						both = true;
					} else if (line.contains("#PAGES")) {
						both = false;
					} else {
						if (both) {
							all.add(line.trim().split("\\t",2));
						} else {
							page.add(line.trim().split("\\t",2));
						}
					}
				}
			}
			inLines.close();
			generalCodes = all.toArray(new String[all.size()][2]);
			pageCodes = page.toArray(new String[page.size()][2]);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}	
	}
	
	private void doSave() {
		File mapOutFile = new File(volume.getFileID() + "-pagemap.tsv");
		try {
			BufferedWriter output = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(mapOutFile),"UTF-8"));
			output.write("");
			Integer keys[] = getIterableKeys(codeDictionary.keySet());
			for(int i=0;i<keys.length;i++){
				output.append(volume.getHTID() + "\t" + keys[i].toString() + "\t" + codeDictionary.get(keys[i]) + "\n");
			}
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
