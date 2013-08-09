package gui;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

public class RangeEdit extends JDialog {
	
	private JLabel pageStartLabel,pageEndLabel,partStartLabel,partEndLabel;
	private JTextField pageStartField,pageEndField,partStartField,partEndField;
	private JButton accept, cancel;
	private JPanel fieldsPanel,buttonsPanel;
	private Boolean result;
	
	//TODO: RESIZE AND ADD BORDERS!
	
	public RangeEdit() {
		setModalityType(ModalityType.APPLICATION_MODAL);
		setAlwaysOnTop(true);
		setLocationRelativeTo(null);
		setResizable(false);
		drawGUI();
		defineListeners();
		result = false;
	}
		
	public void drawGUI () {
		// Set shared UI size objects
		Dimension objectSize = new Dimension(100,30);
		
		// Set layout managers & dialog window size
		setSize(200,200);
		setLayout(new BorderLayout());
		fieldsPanel = new JPanel(new GridLayout(4,2,5,5));
		fieldsPanel.setBorder(new EmptyBorder(5, 8, 5, 5));
		buttonsPanel = new JPanel();
		buttonsPanel.setLayout(new BoxLayout(buttonsPanel,BoxLayout.X_AXIS));
		buttonsPanel.setBorder(new EmptyBorder(5, 8, 5, 5));
		
		// Initialize & configure objects 
		pageStartLabel = new JLabel("Page Start:");
		pageStartLabel.setPreferredSize(objectSize);
		pageEndLabel = new JLabel("Page End:");
		pageEndLabel.setPreferredSize(objectSize);
		partStartLabel = new JLabel("Part Start:");
		partStartLabel.setPreferredSize(objectSize);
		partEndLabel = new JLabel("Part End:");
		partEndLabel.setPreferredSize(objectSize);
		pageStartField = new JTextField();
		pageStartField.setPreferredSize(objectSize);
		pageEndField = new JTextField();
		pageEndField.setPreferredSize(objectSize);
		partStartField = new JTextField();
		partStartField.setPreferredSize(objectSize);
		partEndField = new JTextField();
		partEndField.setPreferredSize(objectSize);
		accept = new JButton("Accept");
		cancel = new JButton("Cancel");
		
		//Add objects in pairs to the field/label grid panel
		fieldsPanel.add(pageStartLabel);
		fieldsPanel.add(pageStartField);
		fieldsPanel.add(pageEndLabel);
		fieldsPanel.add(pageEndField);
		fieldsPanel.add(partStartLabel);
		fieldsPanel.add(partStartField);
		fieldsPanel.add(partEndLabel);
		fieldsPanel.add(partEndField);
		
		//Add buttons to button box panel
		buttonsPanel.add(Box.createHorizontalGlue());
		buttonsPanel.add(accept);
		buttonsPanel.add(cancel);
		buttonsPanel.add(Box.createHorizontalGlue());
		
		//Add panels to dialog layout
		add(fieldsPanel,BorderLayout.CENTER);
		add(buttonsPanel,BorderLayout.SOUTH);
		
	}
	
	private void defineListeners() {
		accept.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				result = true;
				dispose();
			}
		});
		
		cancel.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				result = false;
				dispose();
			}
		});
	}
	
	public void setRange (String[] range) {
		pageStartField.setText(range[0]);
		pageEndField.setText(range[1]);
		partStartField.setText(range[2]);
		partEndField.setText(range[3]);
	}
	
	public String[] getRange () {
		String[] range = new String[4];
		range[0] = pageStartField.getText();
		range[1] = pageEndField.getText();
		range[2] = partStartField.getText();
		range[3] = partEndField.getText();
		return range;
	}
	
	public Boolean getResult () {
		return result;
	}
	
}
