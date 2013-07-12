package gui;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.border.EmptyBorder;

public class HeaderEdit extends JDialog {
	
	private JTextArea headingF;
	private JTextField relationF;
	private JScrollPane headingSP;
	private JLabel headingL, relationL;
	private JButton accept,cancel;
	private JPanel pfields,pbuttons,pheading,prelation;
	private Boolean result;

	public HeaderEdit() {
		setSize(300, 300);
		setModalityType(ModalityType.APPLICATION_MODAL);
		setLocationRelativeTo(getParent());
		DrawGUI();
		DefineButtons();
		result = false;
	}
	
	private void DrawGUI() {
		/*
		 * Create elements in nested layouts as follows:
		 * Entire dialog 
		 * - Text input and labels
		 * - - Heading TextArea and label
		 * - - Relation TextField and label
		 * - Buttons and labels
		 */
		
		// Create the text boxes and labels for heading & relation edits
		pfields = new JPanel();
		pfields.setLayout(new BorderLayout());
		pheading = new JPanel();
		headingL = new JLabel("Heading:");
		headingF = new JTextArea();
		headingSP = new JScrollPane(headingF);
		pheading.setLayout(new BorderLayout());
		pheading.setBorder(new EmptyBorder(10, 10, 10, 10));
		pheading.add(headingL,BorderLayout.NORTH);
		pheading.add(headingSP,BorderLayout.CENTER);
		pfields.add(pheading,BorderLayout.CENTER);
		prelation = new JPanel();
		prelation.setLayout(new BoxLayout(prelation,BoxLayout.X_AXIS));
		relationL = new JLabel("Relation:");
		relationF = new JTextField();
		prelation.add(Box.createHorizontalGlue());
		prelation.add(relationL);
		prelation.add(relationF);
		prelation.add(Box.createHorizontalGlue());
		pheading.add(prelation,BorderLayout.SOUTH);
		
		// Create the buttons
		pbuttons = new JPanel();
		pbuttons.setLayout(new BoxLayout(pbuttons,BoxLayout.X_AXIS));
		accept = new JButton("Accept");
		cancel = new JButton("Cancel");
		pbuttons.add(Box.createHorizontalGlue());
		pbuttons.add(accept);
		pbuttons.add(cancel);
		pbuttons.add(Box.createHorizontalGlue());
		pbuttons.setBorder(new EmptyBorder(5, 5, 5, 5));
		
		// Set groups into dialog's primary layout manager
		setLayout(new BorderLayout());
		add(pheading,BorderLayout.CENTER);
		add(pbuttons,BorderLayout.SOUTH);		
	}
	
	private void DefineButtons() {
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
		headingF.setText(single);
	}
	
	String[] getHeading () {
		String[] output = headingF.getText().split("\\n");
		for (int i=0;i<output.length;i++) {
			if (output[i].startsWith("% ") || output[i].startsWith("%")) {
				continue;
			}
			output[i] = "% " + output[i];
		}
		return output;
	}
	
	void setRelation (String input) {
		relationF.setText(input);
	}
	
	String getRelation () {
		return relationF.getText();
	}
	
	Boolean getResult () {
		return result;
	}
}
