package gui;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

public class HeaderEdit extends JDialog {
	
	private JTextArea headingField;
	private JTextField relationField;
	private JScrollPane headingScroll;
	private JLabel headingLabel, relationLabel;
	private JButton accept,cancel;
	private JPanel fieldsPanel,buttonsPanel,headingPanel,relationPanel;
	private Boolean result;

	public HeaderEdit() {
		setModalityType(ModalityType.APPLICATION_MODAL);
		setAlwaysOnTop(true);
		setLocationRelativeTo(null);
		setResizable(false);
		drawGUI();
		defineListeners();
		result = false;
	}
	
	private void drawGUI() {
		/*
		 * Create elements in nested layouts as follows:
		 * Entire dialog 
		 * - Text input and labels
		 * - - Heading TextArea and label
		 * - - Relation TextField and label
		 * - Buttons and labels
		 */
		setSize(300, 300);
		
		// Create the text boxes and labels for heading & relation edits
		fieldsPanel = new JPanel();
		fieldsPanel.setLayout(new BorderLayout());
		headingPanel = new JPanel();
		headingLabel = new JLabel("Heading:");
		headingField = new JTextArea();
		headingScroll = new JScrollPane(headingField);
		headingPanel.setLayout(new BorderLayout());
		headingPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
		headingPanel.add(headingLabel,BorderLayout.NORTH);
		headingPanel.add(headingScroll,BorderLayout.CENTER);
		fieldsPanel.add(headingPanel,BorderLayout.CENTER);
		relationPanel = new JPanel();
		relationPanel.setLayout(new BoxLayout(relationPanel,BoxLayout.X_AXIS));
		relationLabel = new JLabel("Relation:");
		relationField = new JTextField();
		relationPanel.add(Box.createHorizontalGlue());
		relationPanel.add(relationLabel);
		relationPanel.add(relationField);
		relationPanel.add(Box.createHorizontalGlue());
		headingPanel.add(relationPanel,BorderLayout.SOUTH);
		
		// Create the buttons
		buttonsPanel = new JPanel();
		buttonsPanel.setLayout(new BoxLayout(buttonsPanel,BoxLayout.X_AXIS));
		accept = new JButton("Accept");
		cancel = new JButton("Cancel");
		buttonsPanel.add(Box.createHorizontalGlue());
		buttonsPanel.add(accept);
		buttonsPanel.add(cancel);
		buttonsPanel.add(Box.createHorizontalGlue());
		buttonsPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
		
		// Set groups into dialog's primary layout manager
		setLayout(new BorderLayout());
		add(headingPanel,BorderLayout.CENTER);
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
	
	void setHeading (String[] input) {
		String single = new String();
		for(int i=0;i<input.length;i++) {
			single += input[i];
			if (i<input.length-1){
				single += "\n";
			}
		}
		headingField.setText(single);
	}
	
	String[] getHeading () {
		String[] output = headingField.getText().split("\\n");
		for (int i=0;i<output.length;i++) {
			if (output[i].startsWith("% ") || output[i].startsWith("%")) {
				continue;
			}
			output[i] = "% " + output[i];
		}
		return output;
	}
	
	void setRelation (String input) {
		relationField.setText(input);
	}
	
	String getRelation () {
		return relationField.getText();
	}
	
	Boolean getResult () {
		return result;
	}
}
