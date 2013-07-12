package gui;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class RecordViewer extends JDialog {
	/**
	 * TODO: Documentation
	 */
	
	JLabel htidL, volnumL, callnumL, authorL, titleL, publishL, dateL, copyL, subjectL;
	JTextField htidF, volnumF, callnumF, authorF, dateF, copyF;
	JTextArea titleF, publishF, subjectF;
	JScrollPane titleSP, publishSP, subjectSP;
	JButton close;
	JPanel labelP, fieldP;
	
	public RecordViewer (String[] record) {
		setModalityType(ModalityType.APPLICATION_MODAL);
		setLocationRelativeTo(getParent());
		setResizable(false);
		// Pass record data to relevant fields & add to ArrayList for management
		htidF = new JTextField(record[0]);
		volnumF = new JTextField(record[1]);
		callnumF = new JTextField(record[2]);
		authorF = new JTextField(record[3]);
		titleF = new JTextArea(record[4]);
		publishF = new JTextArea(record[5]);
		dateF = new JTextField(record[6]);
		copyF = new JTextField(record[7]);
		subjectF = new JTextArea(record[8]);
		DrawGUI();
		DefineButtons();
	}
	
	private void DrawGUI() {
		// UI layout objects
		GridBagConstraints labels = new GridBagConstraints();
		GridBagConstraints fields = new GridBagConstraints();
		GridBagConstraints full = new GridBagConstraints();
		Dimension area_size = new Dimension(269,75);
		Dimension field_size = new Dimension(275,25);
		Dimension label_size_small = new Dimension(100,25);
		Dimension label_size_big = new Dimension(100,75);
		
		// Set layout managers & column+cell properties
		setLayout(new GridBagLayout());
		setSize(440,500);
		labels.gridwidth = 1;
		labels.gridx = 0;
		fields.gridwidth = 3;
		fields.gridx = 1;
		fields.insets = new Insets(3,3,3,3);
		full.gridwidth = 4;
		full.gridx = 0;
		
		//Initialize & configure static components
		htidL = new JLabel("HTID:");
		htidL.setPreferredSize(label_size_small);
		volnumL = new JLabel("Volume ID:");
		volnumL.setPreferredSize(label_size_small);
		callnumL = new JLabel("Call Number:");
		callnumL.setPreferredSize(label_size_small);
		authorL = new JLabel("Author:");
		authorL.setPreferredSize(label_size_small);
		titleL = new JLabel("Title:");
		titleL.setPreferredSize(label_size_big);
		publishL = new JLabel("Publisher:");
		publishL.setPreferredSize(label_size_big);
		dateL = new JLabel("Date:");
		dateL.setPreferredSize(label_size_small);
		copyL = new JLabel("Copy:");
		copyL.setPreferredSize(label_size_small);
		subjectL = new JLabel("Subject:");
		subjectL.setPreferredSize(label_size_big);
		close = new JButton("Close");
		
		//Initialize & configure container objects
		titleSP = new JScrollPane(titleF);
		titleSP.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		titleSP.setPreferredSize(area_size);
		titleF.setLineWrap(true);
		titleF.setWrapStyleWord(true);
		titleF.setEditable(false);
		publishSP = new JScrollPane(publishF);
		publishSP.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		publishSP.setPreferredSize(area_size);
		publishF.setLineWrap(true);
		publishF.setWrapStyleWord(true);
		publishF.setEditable(false);
		subjectSP = new JScrollPane(subjectF);		
		subjectSP.setHorizontalScrollBarPolicy(ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
		subjectSP.setPreferredSize(area_size);
		subjectF.setLineWrap(true);
		subjectF.setWrapStyleWord(true);
		subjectF.setEditable(false);
		
		//Configure uncontained textfields
		htidF.setPreferredSize(field_size);
		htidF.setEditable(false);
		volnumF.setPreferredSize(field_size);
		volnumF.setEditable(false);
		callnumF.setPreferredSize(field_size);
		callnumF.setEditable(false);
		authorF.setPreferredSize(field_size);
		authorF.setEditable(false);
		dateF.setPreferredSize(field_size);
		dateF.setEditable(false);
		copyF.setPreferredSize(field_size);
		copyF.setEditable(false);
		
		//Add pairs of objects to columns
		labels.gridy = 0;
		fields.gridy = 0;
		add(htidL,labels);
		add(htidF,fields);
		labels.gridy = 1;
		fields.gridy = 1;
		add(volnumL,labels);
		add(volnumF,fields);
		labels.gridy = 2;
		fields.gridy = 2;
		add(callnumL,labels);
		add(callnumF,fields);
		labels.gridy = 3;
		fields.gridy = 3;
		add(authorL,labels);
		add(authorF,fields);
		labels.gridy = 4;
		fields.gridy = 4;
		add(titleL,labels);
		add(titleSP,fields);
		labels.gridy = 5;
		fields.gridy = 5;
		add(publishL,labels);
		add(publishSP,fields);
		labels.gridy = 6;
		fields.gridy = 6;
		add(dateL,labels);
		add(dateF,fields);
		labels.gridy = 7;
		fields.gridy = 7;
		add(copyL,labels);
		add(copyF,fields);
		labels.gridy = 8;
		fields.gridy = 8;
		add(subjectL,labels);
		add(subjectSP,fields);
		full.gridy = 9;
		add(close,full);
	}
	
	private void DefineButtons() {
		close.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				dispose();
			}
		});
	}
}
